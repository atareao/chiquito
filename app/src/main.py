#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2021 Lorenzo Carbonell <a.k.a. atareao>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sqlite3
import datetime
import random
from flask import Flask, jsonify, make_response, abort, url_for

app = Flask(__name__)


@app.route('/status', methods=['GET'])
def get_status():
    return make_response(jsonify({'status': 'Up and running'}), 200)


def create_joke(id, author, value, created_at, updated_at):
    created_at = datetime.datetime.fromtimestamp(created_at).isoformat()
    updated_at = datetime.datetime.fromtimestamp(updated_at).isoformat()
    return {'id': id,
            'author': author,
            'value': value,
            'url': url_for('get_joke', joke_id=id, _external=True),
            'created_at': created_at,
            'updated_at': updated_at}


def select(sqlquery, one=False):
    conn = sqlite3.connect('frases.db')
    cursor = conn.cursor()
    cursor.execute(sqlquery)
    if one:
        return cursor.fetchone()
    return cursor.fetchall()


def select_joke(sqlquery, one=False):
    data = select(sqlquery, one)
    if one:
        i = data
        joke = create_joke(i[0], i[1], i[2], i[3], i[4])
        return joke
    else:
        jokes = []
        for i in data:
            joke = create_joke(i[0], i[1], i[2], i[3], i[4])
            jokes.append(joke)
        return jokes


@app.route('/api/1.0/jokes', methods=['GET'])
def get_jokes():
    sqlquery = 'SELECT * FROM JOKES'
    return jsonify(select_joke(sqlquery)), 201


@app.route('/api/1.0/jokes/<int:joke_id>', methods=['GET'])
def get_joke(joke_id):
    sqlquery = 'SELECT * FROM JOKES WHERE ID={}'.format(joke_id)
    result = select_joke(sqlquery, True)
    if result:
        return jsonify(result), 201
    abort(404)


@app.route('/api/1.0/jokes/random', methods=['GET'])
def get_random():
    sqlquery = 'SELECT COUNT(1) FROM JOKES'
    result = select(sqlquery, True)
    print(result, type(result))
    id = random.randint(1, result[0])
    return get_joke(id)


@app.errorhandler(404)
def not_found(error):
    msg = str(error)
    return make_response(jsonify({'status': 'error', 'msg': msg}), 404)


def get():
    conn = sqlite3.connect('../frases.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM JOKES')
    jokes = []
    for i in cursor.fetchall():
        print(i)
