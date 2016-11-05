import os
from random import randint
from flask import Flask, abort, request, jsonify
from jsonschema import validate, ValidationError
import requests
import logging
from logging import StreamHandler
import psycopg2
import urlparse
import time

from texts import VERSION
import texts

app = Flask(__name__)
app.logger.setLevel(logging.INFO)
app.logger.addHandler(StreamHandler())

update_schema = {
    'type': 'object',
    'properties': {
        'update_id': {'type': 'integer'},
        'message': {
            'type': 'object',
            'properties': {
                'message_id': {'type': 'integer'},
                'text': {'type': 'string'},
                'chat': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'}
                    },
                    "required": ["id"]
                }
            },
            "required": ["message_id"]
        },
    },
    "required": ["update_id"]
}

def new_conn():
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    return conn


def talk_with_user():
    return texts.BASE_ANSWER


def log_request(chat_id):
    try:
        conn = new_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO CHATS (CHAT_ID, LAST_TS) \
             VALUES ('{0}', {1})".format(chat_id, int(time.time()))
        )
        conn.commit()
        cur.close()
        conn.close()
    except:
        conn = new_conn()
        cur = conn.cursor()
        cur.execute(
            "UPDATE CHATS set LAST_TS = {1} \
             where CHAT_ID='{0}'".format(chat_id, int(time.time()))
        )
        conn.commit()
        cur.close()
        conn.close()


@app.route('/hodor/<token>', methods=['POST'])
def hodor(token):
    if os.environ.get('TELEGRAM_TOKEN') is None:
        abort(500)
    if token != os.environ.get('TELEGRAM_TOKEN'):
        abort(400, extra='token does not match')
    try:
        validate(request.json, update_schema)
    except ValidationError as detail:
        abort(400, detail.args[0])
    app.logger.info('chat id={0}, text={1}'.format(request.json["message"]["chat"]["id"], request.json["message"]["text"]))
    chat_id = request.json["message"]["chat"]["id"]
    log_request(chat_id)
    res = {
        'chat_id': chat_id,
        'text': talk_with_user()
    }
    requests.post('https://api.telegram.org/bot{0}/SendMessage'.format(os.environ.get('TELEGRAM_TOKEN')), data=res)
    return jsonify(res), 200

@app.route('/create_db')
def create_db():
    conn = new_conn()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE CHATS
           (CHAT_ID        TEXT PRIMARY KEY     NOT NULL,
            LAST_TS        INT     NOT NULL);''')
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"result":"Table created successfully"})


def get_all_chats():
    conn = new_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT CHAT_ID, LAST_TS  from CHATS"
    )
    rows = cur.fetchall()
    result = []
    for row in rows:
        chat_id, last_ts = row[0], row[1]
        result.append({"CHAT_ID":chat_id, "LAST_TS":last_ts})
    cur.close()
    conn.close()
    return result

@app.route('/show_chats')
def show_chats():
    rows = get_all_chats()
    return jsonify({"CHATS":rows})

@app.route("/anons_update")
def anons_update():
    count = 0
    for chat_info in get_all_chats():
        chat_id = chat_info["CHAT_ID"]
        res = {
            'chat_id': chat_id,
            'text': texts.UPDATE_ANONS
        }
        requests.post('https://api.telegram.org/bot{0}/SendMessage'.format(os.environ.get('TELEGRAM_TOKEN')), data=res)
        count += 1
    return jsonify({"update_setn": count})

if __name__ == '__main__':
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])

    app.run(host='0.0.0.0', port=int(os.environ.get('PORT')))
