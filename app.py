from flask import Flask, render_template, request, g
import sqlite3
DB_NAME = ".app.db"
DATABASE = "./app.sql"

app = Flask(__name__)


@app.route('/hello/<name>/<firstname>')
def hello(name=None, firstname=None):
    return render_template('hello.html', name=name, firstname=firstname)

'''with open(DATABASE) as fd:
    print("Database connection...")
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.executescript(fd.read())
    print("Database initialized with success!")
    connection.close()'''

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_NAME)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv