from flask import Flask, render_template, request, make_response
import re

app = Flask(__name__)

application = app

def validate_phone_number(phone_number):
    valid_str = "01234567890()-+. "
    num_str = "01234567890"
    num_count = 0
    for letter in phone_number:
        if letter not in valid_str:
            return (
                "Недопустимый ввод. В номере телефона встречаются недопустимые символы.",
                "invalid-feedback",
                "is-invalid",
            )
        if letter in num_str:
            num_count += 1
    if num_count != 10 and num_count != 11:
        return (
            "Недопустимый ввод. Неверное количество цифр.",
            "invalid-feedback",
            "is-invalid",
        )
    regexp1 = re.compile(r"^\+7 \((\d{3})\) (\d{3})-(\d{2})-(\d{2})$")
    regexp2 = re.compile(r"^8\((\d{3})\)(\d{3})(\d{2})(\d{2})$")
    regexp3 = re.compile(r"(\d{3})\.(\d{3})\.(\d{2})\.(\d{2})")
    r1 = regexp1.match(phone_number)
    r2 = regexp2.match(phone_number)
    r3 = regexp3.match(phone_number)
    m = []
    if r1:
        m = r1.groups()
    elif r2:
        m = r2.groups()
    elif r3:
        m = r3.groups()
    else:
        return (
            "Недопустимый ввод. Номер записан в некорректном формате",
            "invalid-feedback",
            "is-invalid",
        )
    return "8-" + "-".join(m), "valid-feedback", "is-valid"


@app.route("/")
def index():
    msg = "Hello world"
    return render_template("index.html", msg=msg)


@app.route("/argv")
def argv():
    return render_template("argv.html")


@app.route("/headers")
def headers():
    return render_template("headers.html")

@app.route("/cookie")
def cookie():
    resp = make_response(render_template("cookie.html"))
    if "user" in request.cookies:
        resp.delete_cookie("user")
    else:
        resp.set_cookie("user", "NoName")
    return resp

@app.route("/phone_form", methods=["POST", "GET"])
def phone_form():
    kwargs = {}
    if request.method == "POST":
        num = request.form.get("phone_num")
        message, block_class, field_class = validate_phone_number(num)
        kwargs["message"] = message
        kwargs["class"] = block_class
        kwargs["field_class"] = field_class
    return render_template("phone_form.html", **kwargs)

if __name__ == '__main__':
    app.run(debug=True)