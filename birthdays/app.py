import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # get form values
        name = request.form["name"]
        month = request.form["month"]
        day = request.form["day"]

        #create the insert query pattern
        insert_query = "INSERT INTO birthdays (name, month, day) VALUES(?,?,?)"
        # execute query
        db.execute(insert_query,name,month,day)

        return redirect("/")

    else:
        # get birthdays and send them to index
        birthdays = db.execute("SELECT * FROM birthdays")

        return render_template("index.html",birthdays=birthdays)


