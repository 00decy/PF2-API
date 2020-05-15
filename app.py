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
    trait_name = request.args.get('trait')

    query = 'SELECT * FROM feats WHERE'
    to_query = []

    if trait_name:
        # query traits table for trait id
        trait_id = db.execute('SELECT id FROM traits WHERE name=?',
                              [trait_name]).fetchone()

        # deal with empty query result
        if trait_id:
            # for if the trait name exists in our table
            trait_id = trait_id['id']
        else:
            # for if it doesn't
            # this will mean an empty results list is returned to the user
            trait_id = 0

        # alter query to filter by trait
        query = ('SELECT * FROM feats JOIN feat_traits ON feats.id='
                 + 'feat_traits.feat_id WHERE feat_traits.trait_id=? AND')
        to_query.append(trait_id)
    if id:
        # adds id to query
        if trait_name:
            query += ' feats.id=? AND'
        else:
            query += ' id=? AND'
        to_query.append(int(id))
    if source:
        # adds source to query
        if trait_name:
            query += ' feats.source LIKE ? AND'
        else:
            query += ' source LIKE ? AND'
        to_query.append(source + '%')
    if name:
        # add name to query
        if trait_name:
            query += ' feats.name=? AND'
        else:
            query += ' name=? AND'
        to_query.append(name)
    if action:
        # add action to query
        if trait_name:
            query += ' feats.action=? AND'
        else:
            query += ' action=? AND'
        to_query.append(action)
    if level:
        # add level to query
        if trait_name:
            query += ' feats.level=? AND'
        else:
            query += ' level=? AND'
        to_query.append(int(level))
    if archetype:
        # add archetype to query
        if trait_name:
            query += ' feats.archetype=? AND'
        else:
            query += ' archetype=? AND'
        to_query.append(archetype)

    if not (id or source or name or action or level or archetype
            or trait_name):
        # queries traits table for all rows
        rows = db.execute('SELECT * FROM feats').fetchall()
    else:
        # queries traits table based on uery parameters
        rows = db.execute(query[:-4] + ';', to_query).fetchall()

    # need the traits for each feat
    for row in rows:
        # clean up dict for trait queries
        if trait_name:
            del row['trait_id']
            del row['trait_value']
            del row['feat_id']
        # queries traits join feat_traits table by feat_id
        feat_id = int(row['id'])
        trait_rows = db.execute('SELECT * FROM traits '
                                + 'JOIN feat_traits ON traits.id='
                                + 'feat_traits.trait_id '
                                + 'WHERE feat_traits.feat_id=?',
                                [feat_id]).fetchall()

        trait_names = list()
        for trait_row in trait_rows:
            # add trait name, and value if applicable
            if trait_row['trait_value']:
                trait_names.append(trait_row['name'] +
                                   ' ' + trait_row['trait_value'])
            else:
                trait_names.append(trait_row['name'])

        # add list of traits to feat
        row['traits'] = trait_names

    response = {'count': len(rows), 'reults': rows}

    # close database connection
    db.close()

    # returns json
    return jsonify(response)
