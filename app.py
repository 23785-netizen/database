from flask import Flask, g, render_template
import sqlite3

DATABASE = 'database.db'

# initialise app
app = Flask(__name__)


# database connection
def get_db():
    db = getattr(g, '_database', None)
    # if there is no database connection, create one
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


# close the database connection when the app context is torn down
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    # if there is a database connection, close it
    if db is not None:
        db.close()


# query the database
def query_db(query, args=(), one=False):
    # execute the query and fetch the results
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    # return the results, either as a single row or a list of rows
    return (rv[0] if rv else None) if one else rv


@app.route("/")
def home():
    # home page- just the ID, Maker, Model and Image URL
    sql = """
                SELECT Car.CarID,Makers.Name,Car.Model,Car.ImageURL
                FROM Car
                JOIN Makers ON Makers.MakerID=Car.MakerID;"""
    # query the database for all cars
    results = query_db(sql)
    return render_template("home.html", results=results)


@app.route("/car/<int:id>")
def car(id):
    # just one car based on the id
    sql = """SELECT * FROM Car
    JOIN Makers ON Makers.MakerID = Car.MakerID
    WHERE Car.CarID = ?;"""
    # query the database for the specific car
    result = query_db(sql, (id,), True)
    # if the car is not found, return a 404 error
    return render_template("car.html", car=result)


# run the app
if __name__ == "__main__":
    app.run(debug=True)
