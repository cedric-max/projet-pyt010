from flask import Flask, request, g, session, redirect, url_for, flash, render_template
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

### CONSTANTS ###
app = Flask(__name__)
SQL_SCRIPT = "./app.sql"
app.config['DATABASE'] = "./app.db"
app.config['SECRET_KEY'] = '57d907f1370fb2b6e5ca21ef55e584ef8240dcdecbfcc35e8389cdd2751e52bb'

### DATABASE OPERATIONS ###

# Initialize database
with open(SQL_SCRIPT) as fd:
    print("Database connection...")
    connection = sqlite3.connect(app.config['DATABASE'])
    cursor = connection.cursor()
    cursor.executescript(fd.read())
    print("Database initialized with success!")
    connection.close()

# Connect and get database
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

### ROUTES ###
@app.route("/")
def index():
    user_id = session.get('user_id')

    if user_id is None:
        return redirect(url_for('register'))
    else:
        todos = get_db().execute(
            "SELECT oid, ToDo FROM todos WHERE UserId = ?", (user_id,)
        ).fetchall()
        listToDo = []
        for todo in todos :
            row = {"id" : todo['rowid'], "todo" : todo['ToDo']}
            listToDo.append(row)
    # return listToDo;
    return render_template('index.html', todoTab=listToDo);

@app.route("/register", methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT oid, UserName, UserPassword FROM users WHERE UserName = ?;', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['UserPassword'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['rowid']
            return redirect(url_for('index'))

        flash(error)

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('register'))

#Method

#Implementation Add todos
@app.route("/edit/<id>", methods=('GET','POST'))
def edit(id=None):
    todo = {"name" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam id rutrum turpis.","id" : 1}
    return render_template('edit.html', todo=todo)


#Implementation Delete todos
@app.route("/delete/<id>", methods=['POST'])
def delete(id=None):
    todo = {"name" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam id rutrum turpis.","id" : 1}
    return redirect(url_for('test'))


@app.route("/test")
def test():
    todo_list = [{"name" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam id rutrum turpis.","id" : 1},
    {"name" : "Sed malesuada ipsum diam, sed elementum tellus porttitor ut. Aenean ornare turpis eget ligula iaculis, in ullamcorper dolor ultrices","id" : 2},
    {"name" : "Morbi convallis non mauris ut auctor. Integer ac laoreet purus, sit amet lacinia urna. Curabitur nec bibendum libero.","id" : 3}]
    return render_template('index.html', todo_list=todo_list)

if __name__ == "__main__":
    app.run(debug=True)