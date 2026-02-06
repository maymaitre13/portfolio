import os

from flask import Flask, jsonify, render_template as rt, request
from flask_cors import CORS
import get_info as gt

app = Flask(__name__)
CORS(app)

EMAIL_DELIVERY_MODE = os.getenv("EMAIL_DELIVERY_MODE", "mock").strip().lower()


@app.route("/")
def home():
    return rt("index.html")


@app.route("/contact")
def contact():
    return rt("contact.html")


@app.route("/projects")
def projects():
    return rt("projects.html")


@app.route("/health")
def health():
    return jsonify({"status": "ok", "email_delivery_mode": EMAIL_DELIVERY_MODE})


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
    app.run(debug=os.getenv("FLASK_DEBUG", "1") == "1")
