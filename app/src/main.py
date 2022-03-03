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
    """
    Get the status of the api server
    """
    return make_response(jsonify({'status': 'Up and running'}), 200)


def create_joke(joke_id, author, value, created_at, updated_at):
    """
    Create a new joke

    :param joke_id integer: The id of the joke
    :param author str: The author of the joke
    :param value str: The joke
    :param created_at integer: the timestamp when created
    :param updated_at integer: the timestamp when updated
   """
    created_at = datetime.datetime.fromtimestamp(created_at).isoformat()
    updated_at = datetime.datetime.fromtimestamp(updated_at).isoformat()
    return {'id': joke_id,
            'author': author,
            'value': value,
            'url': url_for('get_joke', joke_id=joke_id, _external=True),
            'created_at': created_at,
            'updated_at': updated_at}


def select(sqlquery, one=False):
    """
    Generic sql query

    :param sqlquery str: sql query
    :param one bool: if wants one or some items
    """
    conn = sqlite3.connect('frases.db')
    cursor = conn.cursor()
    cursor.execute(sqlquery)
    if one:
        return cursor.fetchone()
    return cursor.fetchall()


def select_joke(sqlquery, one=False):
    """
    Select one or several jokes

    :param sqlquery str: the query
    :param one bool: if wants one joke or several
    """
    data = select(sqlquery, one)
    if one:
        i = data
        joke = create_joke(i[0], i[1], i[2], i[3], i[4])
        return joke
    jokes = []
    for i in data:
        joke = create_joke(i[0], i[1], i[2], i[3], i[4])
        jokes.append(joke)
    return jokes


@app.route('/api/1.0/jokes', methods=['GET'])
def get_jokes():
    """
    Get all the jokes

    """
    sqlquery = 'SELECT * FROM JOKES'
    return jsonify(select_joke(sqlquery)), 201


@app.route('/api/1.0/jokes/<int:joke_id>', methods=['GET'])
def get_joke(joke_id):
    """
    Get one joke

    :param joke_id int: The id of the joke
    """
    sqlquery = f"SELECT * FROM JOKES WHERE ID={joke_id}"
    result = select_joke(sqlquery, True)
    if result:
        return jsonify(result), 201
    abort(404)
    return None


@app.route('/api/1.0/jokes/random', methods=['GET'])
def get_random():
    """
    Get a random joke

    """
    sqlquery = 'SELECT COUNT(1) FROM JOKES'
    result = select(sqlquery, True)
    print(result, type(result))
    joke_id = random.randint(1, result[0])
    return get_joke(joke_id)


@app.errorhandler(404)
def not_found(error):
    """
    When not found

    :param error str: A json with the error
    """
    msg = str(error)
    return make_response(jsonify({'status': 'error', 'msg': msg}), 404)


def get():
    """
    Print all the jokes

    """
    conn = sqlite3.connect('../frases.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM JOKES')
    for i in cursor.fetchall():
        print(i)
