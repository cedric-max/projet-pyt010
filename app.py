from flask import Flask
import sqlite3

### CONSTANTS ###
app = Flask(__name__)
DATABASE = "./app.db"
SQL_SCRIPT = "./app.sql"

### DATABASE OPERATIONS ###

# Initialize database
with open(SQL_SCRIPT) as fd:
    print("Database connection...")
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.executescript(fd.read())
    print("Database initialized with success!")
    connection.close()

### ROUTES ###
@app.route("/")
def index():
    return "HELLO WORLD"


if __name__ == "__main__":
    app.run(debug=True)
