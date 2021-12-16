import sqlite3
from flask import Flask, request, g, session, redirect, url_for, flash, render_template
from werkzeug.security import check_password_hash

### CONSTANTS & CONFIG ###
app = Flask(__name__)
SQL_SCRIPT = "./app.sql"
app.config["DATABASE"] = "./app.db"
app.config[
    "SECRET_KEY"
] = "57d907f1370fb2b6e5ca21ef55e584ef8240dcdecbfcc35e8389cdd2751e52bb"

### DATABASE ###

# INITIALIZE
with open(SQL_SCRIPT) as fd:
    # Connect to the database.
    connection = sqlite3.connect(app.config["DATABASE"])
    cursor = connection.cursor()
    # Execute the app.sql script.
    cursor.executescript(fd.read())
    # Close connection.
    connection.close()
    print("Database initialized with success!")


# CONNECT AND GET
def get_db():
    """Connect to database and add it to the g object."""
    if "db" not in g:
        g.db = sqlite3.connect(
            app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


# EXECUTE QUERY AND COMMIT DATA
def execute_query_and_commit(query, parameters):
    """Execute query with parameters and commit"""
    db = get_db()
    db.execute(query, parameters)
    db.commit()


### ROUTES ###


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register page where the user can login. We check if the user & password combination exists in the database. If it does, the user is redirected to the index page. Otherwise we throw an error message."""
    if request.method == "POST":
        # Get user and password from the request form.
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        # Look for the user in the database.
        user = db.execute(
            "SELECT oid, UserName, UserPassword FROM users WHERE UserName = ?",
            (username,),
        ).fetchone()

        # Throw an error if user or password are wrong.
        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["UserPassword"], password):
            error = "Incorrect password."

        # Without error, create the session user_id and redirect to the index page.
        if error is None:
            session.clear()
            session["user_id"] = user["rowid"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("register.html")


@app.route("/logout")
def logout():
    """Logout the user by clearing the session object."""
    session.clear()
    return redirect(url_for("register"))


@app.route("/")
def index():
    """Fetch all the todos of the logged user."""
    user_id = session.get("user_id")
    # Prevent the acces of this route if the user isn't logged.
    if user_id is None:
        return redirect(url_for("register"))
    else:
        # Fetch all the users's todos in the database.
        todos = (
            get_db()
            .execute("SELECT oid, ToDoName FROM todos WHERE UserId = ?", (user_id,))
            .fetchall()
        )
        # Convert the todos to an array of dictionary.
        # Makes it easier to display the todos in the browser.
        todo_list = []
        for todo in todos:
            row = {"id": todo["rowid"], "name": todo["ToDoName"]}
            todo_list.append(row)
    return render_template("index.html", todo_list=todo_list, user_id=user_id)


@app.route("/add", methods=["POST"])
def add():
    """Add a todo to the database"""
    # Get todo name from the request form
    todo_name = request.form["name"]
    # Get user id from the session object
    user_id = session.get("user_id")
    execute_query_and_commit("INSERT INTO todos VALUES (?,?)", (todo_name, user_id))
    return redirect(url_for("index"))


@app.route("/edit/<id>", methods=("GET", "POST"))
def edit(id):
    """Edit todo from the database"""
    if request.method == "POST":
        # Get todo name from the request form
        name = request.form["name"]
        execute_query_and_commit(
            "UPDATE todos SET ToDoName = ? WHERE oid = ?", (name, id)
        )
        return redirect(url_for("index"))

    db = get_db()
    row = db.execute(
        "SELECT rowid, ToDoName FROM todos WHERE oid = ?", (id,)
    ).fetchone()
    todo = {"id": row["rowid"], "name": row["ToDoName"]}
    return render_template("edit.html", todo=todo)


@app.route("/delete/<id>", methods=["POST"])
def delete(id):
    """Delete todo from the database"""
    # Get user is from the session object
    user_id = session.get("user_id")
    execute_query_and_commit(
        "DELETE FROM todos WHERE oid = ? AND UserId = ?", (id, user_id)
    )
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
