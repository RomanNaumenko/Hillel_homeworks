from flask import Flask, request, jsonify
import sqlite3
import datetime

# print(type(datetime.date.today()))
# print(str(datetime.date.today()) == '2022-08-20')

app = Flask(__name__)


def get_db_fetchall(querry: str):
    conn = sqlite3.connect('database_lite.db')
    cursor = conn.execute(querry)
    result = cursor.fetchall()
    conn.close()
    return result


def get_db_fetchone(querry: str):
    conn = sqlite3.connect('database_lite.db')
    cursor = conn.execute(querry)
    result = cursor.fetchone()
    conn.close()
    return result


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.get("/currency")
def currencies():
    res = get_db_fetchall(f"SELECT cur_name, available_amount FROM Currency GROUP BY cur_name")
    return f"<p>Available currencies: {res}</p>"


# @app.get("/currency/<currency_name>")
# def currency(currency_name):
#     res = get_db(f"SELECT * FROM Currency WHERE cur_name = '{currency_name}'")
#     return res

@app.get("/currency/<currency_name>")
def currency(currency_name):
    # res = get_db_fetchall(f"SELECT * FROM Currency WHERE cur_name = '{currency_name}'")
    data_dict = {"Currency name": get_db_fetchone(f"SELECT cur_name FROM Currency WHERE cur_name = '{currency_name}'"),
                 "Currency cost related to USD": get_db_fetchone(
                     f"SELECT relative_cost FROM Currency WHERE cur_name = '{currency_name}'"),
                 "Amount of currency": get_db_fetchone(
                     f"SELECT available_amount FROM Currency WHERE cur_name = '{currency_name}'"),
                 "Last price update": get_db_fetchone(f"SELECT cur_date FROM Currency WHERE cur_name = '{currency_name}'")}
    return data_dict


@app.route("/currency/<currency_name>/rating", methods=["GET", "DELETE", "POST", "PUT"])
def currency_review(currency_name):
    if request.method == "GET":
        res = get_db_fetchall(f"SELECT Currency.cur_name, round(avg(Rating.rating), 2) FROM Rating join Currency "
                              f"WHERE Rating.cur_id = Currency.cur_id AND Currency.cur_name = '{currency_name}' "
                              f"GROUP BY Currency.cur_name")
        return f"Currency name and it`s rating: {res}"
    elif request.method == "DELETE":
        return "<p>DELETE</p>"
    elif request.method == "POST":
        return "<p>POST</p>"
    elif request.method == "PUT":
        return "<p>PUT</p>"
    else:
        return "<p>Method not allowed</p>"


@app.route("/currency/trade/<currency_name_1>/<currency_name_2>", methods=["GET", "POST"])
def trade(currency_name_1, currency_name_2):
    if request.method == "GET":
        res = get_db_fetchall(f"""SELECT round(
        (SELECT relative_cost from Currency Where cur_date = '2022-08-20' and cur_name = '{currency_name_1}')/
        (SELECT relative_cost from Currency Where cur_date = '2022-08-20' and cur_name = '{currency_name_2}'), 2)""")
        return f"<p>Today`s trade price of the {currency_name_1} against the {currency_name_2}: {res}</p>"
    elif request.method == "POST":
        return f"<p>post trade {currency_name_1} and {currency_name_2}</p>"
    else:
        return "<p>Method not allowed</p>"


@app.get("/user")
def all_user_info():
    res = get_db_fetchall(f"SELECT user_id, name, login FROM User")
    return f"<p>Users: {res}</p>"


@app.get("/user/<user_id>")
def specific_user_info(user_id):
    # res = get_db_fetchall(f"SELECT * FROM User WHERE name = '{username}'")
    data_dict = {"Name of the user": get_db_fetchone(f"SELECT name FROM User WHERE user_id = '{user_id}'"),
                 "Login of the user": get_db_fetchone(
                     f"SELECT login FROM User WHERE user_id = '{user_id}'")}
    return f"<p>User info: {data_dict}</p>"


@app.post("/user/transfer")
def transfer():
    return "<p>Info about user transfer</p>"


@app.get("/user/<user_id>/history")
def user_history(user_id):
    data_dict = {"User name": get_db_fetchone(f"SELECT name FROM User WHERE user_id = '{user_id}'"),
                 "Operation number and date": get_db_fetchone(
                     f"SELECT  operation_id, datetime FROM Operation WHERE user='{user_id}'"),
                 "Amount of spent currency": get_db_fetchone(
                     f"SELECT  Operation.spent_amount, Currency.cur_name  FROM Operation join Currency WHERE "
                     f"Operation.user='{user_id}' and Operation.cur_from = Currency.cur_id"),
                 "Amount of gain currency": get_db_fetchone(f"SELECT Operation.gain_amount, Currency.cur_name "
                                                            f"FROM Operation join Currency WHERE Operation.user='{user_id}'"
                                                            f"and Operation.cur_to = Currency.cur_id")}
    return f"<p>{data_dict}</p>"


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
