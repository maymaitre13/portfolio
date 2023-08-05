from flask import Flask, render_template as rt, request
import get_info as gt

app = Flask(__name__)


@app.route("/")
def main():
    return rt("index.html")


@app.route("/contact")
def email():
    return rt("contact.html")


@app.route('/send_email', methods=["POST"])
def send_email():
    state = 0
    f_name = request.form["firstName"]
    l_name = request.form["lastName"]
    t_email = request.form["email"]
    the_email = request.form["the_email"]

    if the_email == "":
        state = 1

    gt.send_email(f_name,l_name, t_email, the_email)
    return rt("validation.html", state=state)


if __name__ == "__main__":
    app.run(debug=True)

