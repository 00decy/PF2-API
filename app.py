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


# def of database configuration
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
    source = request.args.get('source')
    name = request.args.get('name')

    query = 'SELECT * FROM traits WHERE'
    to_query = []

    if id:
        # adds id to query
        query += ' id=? AND'
        to_query.append(int(id))
    if source:
        # adds source to query
        query += ' source LIKE ? AND'
        to_query.append(source + '%')
    if name:
        # add name to query
        query += ' name=? AND'
        to_query.append(name)

    if not (id or source or name):
        # queries traits table for all rows
        rows = db.execute('SELECT * FROM traits').fetchall()
    else:
        # queries traits table based on uery parameters
        rows = db.execute(query[:-4] + ';', to_query).fetchall()

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
    source = request.args.get('source')
    name = request.args.get('name')
    action = request.args.get('action')
    level = request.args.get('level')
    archetype = request.args.get('archetype')

    query = 'SELECT * FROM feats WHERE'
    to_query = []

    if id:
        # adds id to query
        query += ' id=? AND'
        to_query.append(int(id))
    if source:
        # adds source to query
        query += ' source LIKE ? AND'
        to_query.append(source + '%')
    if name:
        # add name to query
        query += ' name=? AND'
        to_query.append(name)
    if action:
        # add action to query
        query += ' action=? AND'
        to_query.append(action)
    if level:
        # add level to query
        query += ' level=? AND'
        to_query.append(int(level))
    if archetype:
        # add archetype to query
        query += ' archetype=? AND'
        to_query.append(archetype)

    if not (id or source or name or action or level or archetype):
        # queries traits table for all rows
        rows = db.execute('SELECT * FROM feats').fetchall()
    else:
        # queries traits table based on uery parameters
        rows = db.execute(query[:-4] + ';', to_query).fetchall()

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
