#!/usr/bin/env python3
import sqlite3
import datetime
import random
from flask import Flask, jsonify, make_response, abort, url_for

app = Flask(__name__)

def create_joke(id, author, value, created_at, updated_at):
    return {'id': id,
            'author': author,
            'value': value,
            'url': url_for('get_joke', joke_id=id, _external=True),
            'created_at': datetime.datetime.fromtimestamp(created_at).isoformat(),
            'updated_at': datetime.datetime.fromtimestamp(updated_at).isoformat()}
 
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
    return make_response(jsonify({'error': 'Not found'}), 404)

def get():
    conn = sqlite3.connect('../frases.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM JOKES')
    jokes = []
    for i in cursor.fetchall():
        print(i)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
