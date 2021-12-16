from flask import Flask, request, g, session, redirect, url_for, flash, render_template
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

### CONSTANTS ###
app = Flask(__name__)
SQL_SCRIPT = "./app.sql"
app.config["DATABASE"] = "./app.db"
app.config[
    "SECRET_KEY"
] = "57d907f1370fb2b6e5ca21ef55e584ef8240dcdecbfcc35e8389cdd2751e52bb"

### DATABASE ###

# Initialize database
with open(SQL_SCRIPT) as fd:
    connection = sqlite3.connect(app.config["DATABASE"])
    cursor = connection.cursor()
    cursor.executescript(fd.read())
    print("Database initialized with success!")
    connection.close()

# Connect and get database
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


### ROUTES ###
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT oid, UserName, UserPassword FROM users WHERE UserName = ?",
            (username,),
        ).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["UserPassword"], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["user_id"] = user["rowid"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("register"))

@app.route("/")
def index():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect(url_for("register"))
    else:
        todos = (
            get_db()
            .execute("SELECT oid, ToDoName FROM todos WHERE UserId = ?", (user_id,))
            .fetchall()
        )
        todo_list = []
        for todo in todos:
            row = {"id": todo["rowid"], "name": todo["ToDoName"]}
            todo_list.append(row)
    return render_template("index.html", todo_list=todo_list, user_id=user_id)

@app.route("/add", methods=["POST"])
def add():
    todo_name = request.form["name"]
    user_id = session.get("user_id")
    db = get_db()
    db.execute("INSERT INTO todos VALUES (?,?)", (todo_name, user_id))
    db.commit()
    return redirect(url_for("index"))

@app.route("/edit/<id>", methods=("GET", "POST"))
def edit(id):
    if request.method == "POST":
        name = request.form["name"]
        db = get_db()
        db.execute("UPDATE todos SET ToDoName = ? WHERE oid = ?", (name, id))
        db.commit()
        return redirect(url_for("index"))

    db = get_db()
    todo_row = db.execute(
        "SELECT rowid, ToDoName FROM todos WHERE oid = ?", (id,)
    ).fetchone()
    todo = {"id": todo_row["rowid"], "name": todo_row["ToDoName"]}
    return render_template("edit.html", todo=todo)

@app.route("/delete/<id>", methods=["POST"])
def delete(id):
    user_id = session.get("user_id")
    db = get_db()
    db.execute("DELETE FROM todos WHERE oid = ? AND UserId = ?", (id, user_id))
    db.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
