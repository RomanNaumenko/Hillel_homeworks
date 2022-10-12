import statistics
import uuid

from flask import Flask, request, jsonify
import sqlite3
import datetime
from statistics import mean
import database
import models
from models import Currency, Rating, User, Operation, Account
from celery_worker import task1
import psycopg2

app = Flask(__name__)

current_date = datetime.date.today().strftime("%Y-%m-%d")


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_db_fetchall(querry: str):
    conn = sqlite3.connect('database_lite.db')
    conn.row_factory = dict_factory
    cursor = conn.execute(querry)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result


def get_db_fetchone(querry: str):
    conn = sqlite3.connect('database_lite.db')
    cursor = conn.execute(querry)
    result = cursor.fetchone()
    conn.close()
    return result


@app.get('/testing')
def testing():
    user_id = 1
    cur_1 = 'UAH'
    cur_2 = 'ZLT'
    amount = 100
    task_obj = task1.apply_async(args=[user_id, cur_1, cur_2, amount])
    return str(task_obj)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.get("/currency")
def currencies():
    database.init_db()
    result = Currency.query.all()
    if not result:
        return "<p>Nothing found</p>"
    return [itm.to_dict() for itm in result]


@app.get("/currency/<currency_name>")
def currency(currency_name):
    database.init_db()
    result = Currency.query.filter_by(cur_name=currency_name).all()
    return [itm.to_dict() for itm in result]


@app.route("/currency/<currency_name>/rating", methods=["GET", "DELETE", "POST", "PUT"])
def currency_review(currency_name):
    database.init_db()
    if request.method == "GET":
        result = Rating.query.filter_by(cur_name=currency_name).all()
        try:
            avg_rating = round(mean([itm.rating for itm in result]), 2)
        except statistics.StatisticsError:
            avg_rating = "No data"

        return {'Currency name': currency_name, 'Average rating': avg_rating}

    elif request.method == "DELETE":
        max_id = Rating.query.filter_by(cur_name=currency_name).order_by(Rating.id).limit(1).first().id
        delete_obj = Rating(cur_name=currency_name, id=max_id)
        database.db_session.delete(delete_obj)
        database.db_session.session.commit()
        return f"{currency_name} latest rating was removed."

    elif request.method == "POST":
        request_data = request.get_json()
        rating = request_data['rating']
        comment = request_data['comment']
        rating_obj = Rating(cur_name=currency_name, rating=rating, comment=comment)
        with database.db_session as session:
            session.add(rating_obj)
            session.commit()
        return f"<p>New rating was added and successfully committed!</p>"

    elif request.method == "PUT":
        return "<p>PUT</p>"

    else:
        return "<p>Method not allowed</p>"


@app.get("/currency/trade/<currency_name_1>/<currency_name_2>")
def course_ups1_to_ups2(currency_name_1, currency_name_2):
    res1 = Currency.query.filter_by(cur_name=currency_name_1, cur_date=current_date).first()
    res2 = Currency.query.filter_by(cur_name=currency_name_2, cur_date=current_date).first()
    return {'value': round(res1.relative_cost / res2.relative_cost, 2)}


@app.post("/currency/trade/<currency_name_1>/<currency_name_2>")
def exchange(currency_name_1, currency_name_2):
    request_data = request.get_json()
    user_id_1 = request_data['data']['id_user_1']
    user_id_2 = request_data['data']['id_user_2']
    amount1 = request_data['data']['amount_currency_1']

    transaction_id = uuid.uuid4()
    database.init_db()
    queue_record = models.TransactionQueue(transaction_id=str(transaction_id), status='In queue')
    database.db_session.add(queue_record)
    database.db_session.commit()

    task_obj = task1.apply_async(args=[user_id_1, user_id_2, currency_name_1, currency_name_2, amount1, transaction_id])
    return {'task_id': str(task_obj)}


@app.get("/user")
def all_user_info():
    database.init_db()
    user_info_dict = {}
    result = User.query.all()
    for items in result:
        user_info_dict[items.name] = items.login
    return f"Users: {user_info_dict}"


@app.get("/user/<user_id>")
def specific_user_info(user_id):
    database.init_db()
    result = User.query.filter_by(user_id=user_id).first()
    return f"User: {result.name}, login: {result.login}"


@app.post("/user/transfer")
def transfer():
    return "<p>Info about user transfer</p>"


@app.get("/user/<user_id>/history")
def user_history(user_id):
    database.init_db()
    data_dict = {}

    res1 = User.query.filter_by(user_id=user_id).first()
    res2 = Operation.query.filter_by(user=user_id).first()
    res3 = database.db_session.query(Operation, Currency).filter(Operation.user == user_id).filter(
        Operation.cur_from == Currency.cur_name).first()
    res4 = database.db_session.query(Operation, Currency).filter(Operation.user == user_id).filter(
        Operation.cur_to == Currency.cur_name).first()

    data_dict["User name"] = res1.name
    data_dict["Operation date"] = res2.datetime
    data_dict["Spent amount"] = res3.Operation.spent_amount
    data_dict["Spent currency"] = res3.Currency.cur_name
    data_dict["Gain amount"] = res4.Operation.gain_amount
    data_dict["Gain currency"] = res4.Currency.cur_name

    return data_dict


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


@app.teardown_appcontext
def shutdown_session(exception=None):
    database.db_session.remove()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
