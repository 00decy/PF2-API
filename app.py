import sqlite3
from flask import Flask, jsonify, redirect, request

# Configure applicaton
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


# Def for dict_factory
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# Configure connection to database
def dbconfig():
    database = sqlite3.connect('pathfinder2.db')
    database.row_factory = dict_factory
    return database


# Default route
@app.route('/')
def index():
    return 'index'

# returns json data for all traits
@app.route('/traits')
def traits():
    db = dbconfig()

    # queries traits table for all rows
    rows = db.execute('SELECT * FROM traits').fetchall()

    response = {'count': len(rows), 'reults': rows}

    # returns json
    return jsonify(response)
