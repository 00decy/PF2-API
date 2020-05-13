import sqlite3
from flask import Flask, jsonify, request

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

# returns json data for traits
@app.route('/traits')
def traits():
    db = dbconfig()

    id = request.args.get('id')

    if id:
        # queries traits table for row by id
        rows = db.execute('SELECT * FROM traits WHERE id=?', (id,)).fetchall()

    else:
        # queries traits table for all rows
        rows = db.execute('SELECT * FROM traits').fetchall()

    response = {'count': len(rows), 'reults': rows}

    # close database connection
    db.close()

    # returns json
    return jsonify(response)

# returns json data for feats
@app.route('/feats')
def feats():
    db = dbconfig()

    id = request.args.get('id')

    if id:
        # queries feats table for row by id
        rows = db.execute('SELECT * FROM feats WHERE id=?', (id,)).fetchall()

    else:
        # queries feats table for all rows
        rows = db.execute('SELECT * FROM feats').fetchall()

    # need the traits for each feat
    for row in rows:
        # queries feat_traits table by feat_id
        feat_id = int(row['id'])
        trait_ids = db.execute('SELECT * FROM feat_traits WHERE feat_id=?',
                               (feat_id,)).fetchall()

        traits = list()
        for trait_id in trait_ids:
            # queries traits table for trait names
            trait = db.execute('SELECT name FROM traits WHERE id=?',
                               (int(trait_id['trait_id']),)).fetchone()['name']

            # add trait name, and value if applicable
            if trait_id['trait_value']:
                traits.append(trait + ' ' + trait_id['trait_value'])
            else:
                traits.append(trait)

        # add list of traits to feat
        row['traits'] = traits

    response = {'count': len(rows), 'reults': rows}

    # close database connection
    db.close()

    # returns json
    return jsonify(response)
