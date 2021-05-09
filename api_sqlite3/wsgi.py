import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True


# A function that accepts the cursor and the original row as a tuple and will return the real result row. 
# This way, you can implement more advanced ways of returning results, such as returning an object that can also access columns by name.
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/users/all', methods=['GET'])
def users_all():
    # First, we connect to the database using our sqlite3 library
    conn = sqlite3.connect('sqlite:///E:\WindowsUserProfile\Desktop\prosjekter\ProjPy\DB\db')

    # You can change this attribute to a callable that accepts the cursor and the original row as a tuple and will return the real result row. 
    # This way, you can implement more advanced ways of returning results, such as returning an object that can also access columns by name.
    # 
    # dict_factory function which is above defined , returns items from the database as dictionaries rather than lists
    conn.row_factory = dict_factory

    # cursor object, which is the object that actually moves through the database to pull our data. 
    cur = conn.cursor()
    all_users = cur.execute('SELECT * FROM User;').fetchall()
    print('*****************************************')
    print(jsonify(all_users))
    print('*****************************************')

    return jsonify(all_users)



@app.route('/api/v1/resources/users', methods=['GET'])
def users_filter():
    query = "SELECT * FROM User WHERE"
    to_filter = []

    if 'username' in request.args:
        username = request.args.get('username')
        query += ' username=? ;'
        to_filter.append(username)
    else:
        return page_not_found(404)

    # First, we connect to the database using our sqlite3 library
    conn = sqlite3.connect('..\\DB\\db')

    # You can change this attribute to a callable that accepts the cursor and the original row as a tuple and will return the real result row. 
    # This way, you can implement more advanced ways of returning results, such as returning an object that can also access columns by name.
    # 
    # dict_factory function which is above defined , returns items from the database as dictionaries rather than lists
    conn.row_factory = dict_factory
    # cursor object, which is the object that actually moves through the database to pull our data. 
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)




# ********************************** Note **********************************
@app.route('/api/v1/resources/notes/all', methods=['GET'])
def notes_all():
    # First, we connect to the database using our sqlite3 library
    conn = sqlite3.connect('..\\DB\\db')

    # You can change this attribute to a callable that accepts the cursor and the original row as a tuple and will return the real result row. 
    # This way, you can implement more advanced ways of returning results, such as returning an object that can also access columns by name.
    # 
    # dict_factory function which is above defined , returns items from the database as dictionaries rather than lists
    conn.row_factory = dict_factory

    # cursor object, which is the object that actually moves through the database to pull our data. 
    cur = conn.cursor()
    all_notes = cur.execute('SELECT * FROM Note;').fetchall()

    return jsonify(all_notes)



@app.route('/api/v1/resources/notes', methods=['GET'])
def notes_filter():
    query = "SELECT * FROM Note WHERE"
    to_filter = []

    query_parameters = request.args
    createdOn = query_parameters.get('createdOn')
    priority = query_parameters.get('priority')
    username = query_parameters.get('username')

    if createdOn:
        query += ' createdOn=? AND'
        to_filter.append(createdOn)
    if priority:
        query += ' priority=? AND'
        to_filter.append(priority)
    if username:
        query += ' username=? AND'
        to_filter.append(username)
    if not (createdOn or priority or username):
        return page_not_found(404)

    query = query[:-4] + ';'

    # First, we connect to the database using our sqlite3 library
    conn = sqlite3.connect('..\\DB\\db')

    # You can change this attribute to a callable that accepts the cursor and the original row as a tuple and will return the real result row. 
    # This way, you can implement more advanced ways of returning results, such as returning an object that can also access columns by name.
    # 
    # dict_factory function which is above defined , returns items from the database as dictionaries rather than lists
    conn.row_factory = dict_factory
    # cursor object, which is the object that actually moves through the database to pull our data. 
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)



# ********************************** Category **********************************
@app.route('/api/v1/resources/categories/all', methods=['GET'])
def categories_all():
    # First, we connect to the database using our sqlite3 library
    conn = sqlite3.connect('..\\DB\\db')

    # You can change this attribute to a callable that accepts the cursor and the original row as a tuple and will return the real result row. 
    # This way, you can implement more advanced ways of returning results, such as returning an object that can also access columns by name.
    # 
    # dict_factory function which is above defined , returns items from the database as dictionaries rather than lists
    conn.row_factory = dict_factory

    # cursor object, which is the object that actually moves through the database to pull our data. 
    cur = conn.cursor()
    all_categories = cur.execute('SELECT * FROM Category;').fetchall()

    return jsonify(all_categories)


app.run(host='127.0.0.1', port=5006)