from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/currency/<currency_name>/review_post", methods=["GET", "DELETE", "POST", "PUT"])
def currency_review(currency_name):
    if request.method == "GET":
        return "<p>GET</p>"
    elif request.method == "DELETE":
        return "<p>DELETE</p>"
    elif request.method == "POST":
        return "<p>POST</p>"
    elif request.method == "PUT":
        return "<p>PUT</p>"
    else:
        return "<p>Method not allowed</p>"


@app.get("/currency/<currency_name>")
def currency(currency_name):
    return f"<p>Currency name: {currency_name}</p>"


@app.route("/currency/trade/<currency_name_1>/<currency_name_2>", methods=["GET", "POST"])
def trade(currency_name_1, currency_name_2):
    if request.method == "GET":
        return f"<p>get trade {currency_name_1} and {currency_name_2}</p>"
    elif request.method == "POST":
        return f"<p>post trade {currency_name_1} and {currency_name_2}</p>"
    else:
        return "<p>Method not allowed</p>"


@app.get("/currency")
def currencies():
    return "<p>Currencies</p>"


@app.get("/user")
def user():
    return "<p>User</p>"


@app.post("/user/transfer")
def user_transfer():
    return "<p>Info about user transfer</p>"


@app.get("/user/history")
def user_history():
    return "<p>Info about user history</p>"


@app.route("/user/deposit", methods=["GET", "POST"])
def user_deposit():
    if request.method == "GET":
        return "<p>Info about user deposit</p>"
    elif request.method == "POST":
        return "<p>Put info about new deposit</p>"


@app.route("/user/deposit/<deposit_id>", methods=["GET", "POST"])
def user_deposit_id(deposit_id):
    if request.method == "GET":
        return f"<p>Info about user deposit: {deposit_id}</p>"
    elif request.method == "POST":
        return f"<p>Put some changes about {deposit_id}</p>"


@app.get("/user/deposit/<currency_name>")
def user_deposit_currency(currency_name):
    return f"<p>Info about {currency_name} deposit rates </p>"


if __name__ == "__main__":
    app.run(debug=True)
