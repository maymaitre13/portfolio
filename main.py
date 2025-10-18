from flask import Flask, render_template as rt, request, jsonify
import get_info as gt

app = Flask(__name__)


@app.route("/")
def main():
    return rt("index.html")


@app.route("/contact")
def email():
    return rt("contact.html")


@app.route("/send_email", methods=["POST"])
def send_email():
    # Support JSON (AJAX) and form submissions with basic validation
    try:
        if request.is_json:
            data = request.get_json(silent=True) or {}
            f_name = data.get("firstName", "").strip()
            l_name = data.get("lastName", "").strip()
            t_email = data.get("email", "").strip()
            the_email = data.get("the_email", "").strip()
            honeypot = data.get("company", "")
        else:
            f_name = request.form.get("firstName", "").strip()
            l_name = request.form.get("lastName", "").strip()
            t_email = request.form.get("email", "").strip()
            the_email = request.form.get("the_email", "").strip()
            honeypot = request.form.get("company", "")

        # Honeypot anti-bot: silently accept
        if honeypot:
            if request.is_json:
                return jsonify({"ok": True}), 200
            return rt("validation.html", state=0)

        if not the_email or len(the_email) < 10:
            if request.is_json:
                return jsonify({"ok": False, "error": "Message too short"}), 400
            return rt("validation.html", state=1)

        try:
            gt.send_email(f_name, l_name, t_email, the_email)
            if request.is_json:
                return jsonify({"ok": True}), 200
            return rt("validation.html", state=0)
        except Exception:
            if request.is_json:
                return jsonify({"ok": False, "error": "Send failure"}), 500
            return rt("validation.html", state=2)
    except Exception:
        if request.is_json:
            return jsonify({"ok": False, "error": "Invalid request"}), 400
        return rt("validation.html", state=2)


if __name__ == "__main__":
    app.run(debug=True)
