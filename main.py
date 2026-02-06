import os
import sys
from datetime import datetime, timedelta
from functools import wraps

from flask import (
    Flask,
    jsonify,
    redirect,
    render_template as rt,
    request,
    session,
    url_for,
)
from flask_cors import CORS
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text
from sqlalchemy.exc import OperationalError
from werkzeug.security import check_password_hash, generate_password_hash

import get_info as gt

app = Flask(__name__)
CORS(app)

os.makedirs(app.instance_path, exist_ok=True)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change-this-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{os.path.join(app.instance_path, 'portfolio.db')}",
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = os.getenv("SESSION_COOKIE_SECURE", "0") == "1"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=8)

EMAIL_DELIVERY_MODE = os.getenv("EMAIL_DELIVERY_MODE", "mock").strip().lower()
MAX_LOGIN_ATTEMPTS = int(os.getenv("LOGIN_MAX_ATTEMPTS", "5"))
LOCKOUT_MINUTES = int(os.getenv("LOGIN_LOCKOUT_MINUTES", "15"))

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = None


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    enabled = db.Column(db.Boolean, nullable=False, default=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    failed_login_attempts = db.Column(db.Integer, nullable=False, default=0)
    lock_until = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)

    def is_locked(self):
        return self.lock_until is not None and self.lock_until > datetime.utcnow()

    def register_failed_login(self):
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= MAX_LOGIN_ATTEMPTS:
            self.failed_login_attempts = 0
            self.lock_until = datetime.utcnow() + timedelta(minutes=LOCKOUT_MINUTES)

    def reset_login_failures(self):
        self.failed_login_attempts = 0
        self.lock_until = None

    @property
    def is_active(self):  # noqa: D401
        return self.enabled


class UserSession(db.Model):
    __tablename__ = "user_sessions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)
    username = db.Column(db.String(120), nullable=False)
    login_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    logout_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(24), nullable=False, default="active")
    login_ip = db.Column(db.String(64), nullable=True)
    logout_ip = db.Column(db.String(64), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)


class AuthEvent(db.Model):
    __tablename__ = "auth_events"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    username = db.Column(db.String(120), nullable=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)
    event_type = db.Column(db.String(48), nullable=False)
    status = db.Column(db.String(32), nullable=False)
    success = db.Column(db.Boolean, nullable=False, default=False)
    reason = db.Column(db.String(255), nullable=True)
    ip_address = db.Column(db.String(64), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    request_path = db.Column(db.String(255), nullable=True)
    session_record_id = db.Column(
        db.Integer, db.ForeignKey("user_sessions.id"), nullable=True, index=True
    )


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("login", next=request.path))


def _client_ip():
    forwarded_for = (request.headers.get("X-Forwarded-For") or "").split(",")[0].strip()
    return forwarded_for or request.remote_addr or ""


def _user_agent():
    value = request.user_agent.string if request.user_agent else ""
    return (value or "")[:255]


def add_auth_event(
    *,
    event_type,
    status,
    success,
    username="",
    user=None,
    reason="",
    session_record_id=None,
):
    event = AuthEvent(
        username=(username or getattr(user, "username", "") or "")[:120],
        user_id=getattr(user, "id", None),
        event_type=event_type[:48],
        status=status[:32],
        success=bool(success),
        reason=(reason or "")[:255] or None,
        ip_address=_client_ip()[:64] or None,
        user_agent=_user_agent()[:255] or None,
        request_path=(request.path or "")[:255] or None,
        session_record_id=session_record_id,
    )
    db.session.add(event)
    return event


def ensure_schema_columns():
    inspector = inspect(db.engine)
    if "users" not in inspector.get_table_names():
        return

    rows = db.session.execute(text("PRAGMA table_info(users)")).all()
    columns = {row[1] for row in rows}
    if "is_admin" not in columns:
        try:
            with db.engine.begin() as conn:
                conn.execute(
                    text("ALTER TABLE users ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT 0")
                )
        except OperationalError as exc:
            if "duplicate column name" not in str(exc).lower():
                raise


def initialize_database():
    db.create_all()
    ensure_schema_columns()

    admin_username = os.getenv("ADMIN_USERNAME", "").strip()
    admin_password = os.getenv("ADMIN_PASSWORD", "")
    admin_is_admin = os.getenv("ADMIN_IS_ADMIN", "1") == "1"

    if not admin_username or not admin_password:
        print(
            "Database initialized. Set ADMIN_USERNAME and ADMIN_PASSWORD "
            "to auto-create an admin user."
        )
        return

    user = User.query.filter_by(username=admin_username).first()
    if user:
        if admin_is_admin and not user.is_admin:
            user.is_admin = True
            db.session.commit()
            print(f"Admin rights granted to '{admin_username}'.")
        print(f"Admin user '{admin_username}' already exists.")
        return

    user = User(username=admin_username, enabled=True, is_admin=admin_is_admin)
    user.set_password(admin_password)
    db.session.add(user)
    db.session.commit()
    print(f"Admin user '{admin_username}' created.")


@app.cli.command("init-db")
def init_db_command():
    initialize_database()


with app.app_context():
    db.create_all()
    ensure_schema_columns()


def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapped(*args, **kwargs):
        if not getattr(current_user, "is_admin", False):
            return redirect(url_for("tools"))
        return view_func(*args, **kwargs)

    return wrapped


@app.route("/")
def home():
    return rt("index.html")


@app.route("/contact")
def contact():
    return rt("contact.html")


@app.route("/projects")
def projects():
    return rt("projects.html")


@app.route("/tools")
def tools():
    return rt("tools.html")


@app.route("/more-tools")
@login_required
def more_tools():
    return rt("more_tools.html")


@app.route("/user-admin")
@admin_required
def user_admin():
    query_text = (request.args.get("q") or "").strip()
    error = request.args.get("error", "")
    success = request.args.get("success", "")

    users_query = User.query
    if query_text:
        users_query = users_query.filter(User.username.ilike(f"%{query_text}%"))

    users = users_query.order_by(User.username.asc()).all()
    recent_auth_events = AuthEvent.query.order_by(AuthEvent.created_at.desc()).limit(50).all()
    recent_sessions = UserSession.query.order_by(UserSession.login_at.desc()).limit(30).all()
    return rt(
        "user_admin.html",
        users=users,
        q=query_text,
        error=error,
        success=success,
        recent_auth_events=recent_auth_events,
        recent_sessions=recent_sessions,
    )


@app.route("/user-admin/create", methods=["POST"])
@admin_required
def user_admin_create():
    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""
    enabled = request.form.get("enabled") == "on"
    is_admin = request.form.get("is_admin") == "on"

    if not username or not password:
        return redirect(url_for("user_admin", error="Username and password are required."))

    if len(password) < 8:
        return redirect(
            url_for("user_admin", error="Password must be at least 8 characters.")
        )

    existing = User.query.filter_by(username=username).first()
    if existing:
        return redirect(url_for("user_admin", error="User already exists."))

    user = User(username=username, enabled=enabled, is_admin=is_admin)
    user.set_password(password)
    db.session.add(user)
    db.session.flush()
    add_auth_event(
        event_type="user_create",
        status="success",
        success=True,
        username=user.username,
        user=user,
        reason=f"created_by:{current_user.username}",
    )
    db.session.commit()
    return redirect(url_for("user_admin", success="User created."))


@app.route("/user-admin/update/<int:user_id>", methods=["POST"])
@admin_required
def user_admin_update(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return redirect(url_for("user_admin", error="User not found."))

    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""
    enabled = request.form.get("enabled") == "on"
    is_admin = request.form.get("is_admin") == "on"

    if not username:
        return redirect(url_for("user_admin", error="Username cannot be empty."))

    duplicate = User.query.filter(User.username == username, User.id != user.id).first()
    if duplicate:
        return redirect(url_for("user_admin", error="Username already in use."))

    if user.id == current_user.id and not is_admin:
        return redirect(url_for("user_admin", error="You cannot remove your own admin role."))

    user.username = username
    user.enabled = enabled
    user.is_admin = is_admin

    if password:
        if len(password) < 8:
            return redirect(
                url_for("user_admin", error="New password must be at least 8 characters.")
            )
        user.set_password(password)

    add_auth_event(
        event_type="user_update",
        status="success",
        success=True,
        username=user.username,
        user=user,
        reason=f"updated_by:{current_user.username}",
    )
    db.session.commit()
    return redirect(url_for("user_admin", success="User updated."))


@app.route("/user-admin/delete/<int:user_id>", methods=["POST"])
@admin_required
def user_admin_delete(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return redirect(url_for("user_admin", error="User not found."))

    if user.id == current_user.id:
        return redirect(url_for("user_admin", error="You cannot delete your own account."))

    target_username = user.username
    db.session.delete(user)
    add_auth_event(
        event_type="user_delete",
        status="success",
        success=True,
        username=target_username,
        reason=f"deleted_by:{current_user.username}",
    )
    db.session.commit()
    return redirect(url_for("user_admin", success="User deleted."))


def _safe_next_url(next_url):
    return bool(next_url) and next_url.startswith("/") and not next_url.startswith("//")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("tools"))

    next_url = request.args.get("next", "")
    error = ""

    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        next_url = request.form.get("next", "")

        user = User.query.filter_by(username=username).first() if username else None

        if user and user.is_locked():
            add_auth_event(
                event_type="login_locked",
                status="locked",
                success=False,
                username=username,
                user=user,
                reason="account_locked",
            )
            db.session.commit()
            error = "Account temporarily locked. Please try again later."
            return rt("login.html", error=error, next_url=next_url), 429

        if not user or not user.enabled or not user.check_password(password):
            reason = "disabled_account" if (user and not user.enabled) else "invalid_credentials"
            if user:
                user.register_failed_login()
            add_auth_event(
                event_type="login_failed",
                status="failed",
                success=False,
                username=username,
                user=user,
                reason=reason,
            )
            db.session.commit()
            error = "Invalid credentials."
            return rt("login.html", error=error, next_url=next_url), 401

        user.reset_login_failures()
        login_user(user)
        session.permanent = True
        new_session = UserSession(
            user_id=user.id,
            username=user.username,
            status="active",
            login_ip=_client_ip()[:64] or None,
            user_agent=_user_agent()[:255] or None,
        )
        db.session.add(new_session)
        db.session.flush()
        session["auth_session_id"] = new_session.id
        add_auth_event(
            event_type="login_success",
            status="success",
            success=True,
            username=user.username,
            user=user,
            reason="credentials_valid",
            session_record_id=new_session.id,
        )
        db.session.commit()

        if _safe_next_url(next_url):
            return redirect(next_url)
        return redirect(url_for("tools"))

    return rt("login.html", error=error, next_url=next_url)


@app.route("/logout")
@login_required
def logout():
    auth_session_id = session.pop("auth_session_id", None)
    username = current_user.username
    user_id = current_user.id

    if auth_session_id:
        active_session = db.session.get(UserSession, int(auth_session_id))
        if active_session and active_session.user_id == user_id:
            active_session.logout_at = datetime.utcnow()
            active_session.status = "closed"
            active_session.logout_ip = _client_ip()[:64] or None

    add_auth_event(
        event_type="logout",
        status="success",
        success=True,
        username=username,
        user=current_user,
        reason="user_logout",
        session_record_id=auth_session_id,
    )
    db.session.commit()
    logout_user()
    return redirect(url_for("home"))


@app.route("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "email_delivery_mode": EMAIL_DELIVERY_MODE,
            "authenticated": bool(current_user.is_authenticated),
        }
    )


def _extract_contact_payload():
    if request.is_json:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form.to_dict(flat=True)

    if not isinstance(data, dict):
        return {}
    return data


@app.route("/send_email", methods=["POST"])
def send_email():
    # Support both JSON (AJAX) and URL-encoded form submissions.
    try:
        data = _extract_contact_payload()
        f_name = data.get("firstName", "").strip()
        l_name = data.get("lastName", "").strip()
        t_email = data.get("email", "").strip()
        the_email = data.get("the_email", "").strip()
        honeypot = data.get("company", "")

        # Honeypot anti-bot: silently accept
        if honeypot:
            return jsonify({"ok": True}), 200

        if not the_email or len(the_email) < 10:
            return jsonify({"ok": False, "error": "Message too short"}), 400

        try:
            if EMAIL_DELIVERY_MODE == "smtp":
                gt.send_email(f_name, l_name, t_email, the_email)
            else:
                app.logger.info("Mock email: from=%s message=%s", t_email, the_email)
            return jsonify({"ok": True}), 200
        except ValueError as exc:
            return jsonify({"ok": False, "error": str(exc)}), 500
        except Exception:
            return jsonify({"ok": False, "error": "Send failure"}), 500
    except Exception:
        return jsonify({"ok": False, "error": "Invalid request"}), 400


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "init-db":
        with app.app_context():
            initialize_database()
    else:
        app.run(debug=os.getenv("FLASK_DEBUG", "1") == "1")
