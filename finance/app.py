import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import enum
import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
# export API_KEY=pk_64a4af4405ee436c84434401cb04648b
db = SQL("sqlite:///finance.db")
# db.execute("PRAGMA foreign_keys = ON")
# db.execute("CREATE TABLE Transactions(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, transaction_type INT, symbol TEXT, share INT, amount NUMERIC, user_id INTEGER NOT NULL,FOREIGN KEY(user_id) REFERENCES users(id))")
# update currentStocks table for foreign id not null
# db.execute("CREATE TABLE CurrentStocks( id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, name TEXT, count INTEGER, user_id INTEGER  NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id))")


# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    # get stocks
    stocks = db.execute(
        "SELECT * FROM CurrentStocks WHERE user_id = ?", session["user_id"])
    total = 0
    symbol_prices = {}
    user = get_current_user()

    # create a dict and iterate through the stocks
    # call get_quote(symbol) to get their latest prices
    for stock in stocks:
        quote = get_quote(stock["symbol"])
        symbol_prices[stock["symbol"]] = quote["price"]
        total += quote["price"] * stock["count"]
    return render_template("index.html", stocks=stocks, symbol_prices=symbol_prices, cash=user["cash"], total=total, usd=usd)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":

        # ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("Provide symbol you must. Yes, hrrmmm.", 400)

        # ensure share was submitted
        elif not request.form.get("shares"):
            return apology("Provide shares you must. Yrsssss.", 400)

        # ensure share is valid number
        elif request.form.get("shares").isdigit() == False:
            return apology("Hrrmmm. Enter positive number you must. Hmm.", 400)

        # set variables
        user = get_current_user()
        balance = user["cash"]
        symbol = request.form.get("symbol").upper()
        shares = int(request.form.get("shares"))
        quote = get_quote(symbol)

        # should be positive
        if shares < 0:
            return apology("Hrrmmm. Enter positive number you must. Hmm.", 400)

        # check for quote
        if quote is None:
            return apology("Has not found, quote.", 400)

        # check for insufficient balance
        if balance == 0:
            return apology("No money you have. Hrmmm.", 400)

        purchase_amount = int(shares) * quote["price"]

        # check if balance is enough
        if balance <= purchase_amount:
            return apology("Not enough money, you have.", 400)

        # common method for handling transactions
        handle_transaction(balance, TransactionType.Buy.value,
                           symbol, shares, purchase_amount, quote["price"])

        # common method for updating stocks
        handle_current_stocks(
            symbol, quote["name"], TransactionType.Buy.value, shares)

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    # get transactions
    transactions = db.execute(
        "SELECT * FROM Transactions WHERE user_id = ?", session["user_id"])
    return render_template("history.html", transactions=transactions, usd=usd, visualize_transaction_type=visualize_transaction_type)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?",
                          request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Empty, symbol field is. Hmmmm.", 400)

        item = get_quote(request.form.get("symbol"))
        if item is None:
            return apology("Has not found, quote.", 400)

        quote = {
            "name": item["name"],
            "price": usd(item["price"]),
            "symbol": item["symbol"]
        }

        return render_template("quoted.html", quote=quote)
    else:

        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not request.form.get("username") or request.form.get("username") == "":
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password") or not request.form.get("confirmation"):
            return apology("must providiee password", 400)

        # Ensure password was submitted
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password does not match", 400)

        # check for duplicate username
        if_user_exist = db.execute(
            "SELECT username FROM users WHERE username LIKE ?", request.form.get("username"))

        if if_user_exist:
            return apology("duplicate username", 400)
        hash = generate_password_hash(request.form.get("password"))

        # insert to query
        insert_query = "INSERT INTO users (username, hash) VALUES(?,?)"
        db.execute(insert_query, request.form.get("username"), hash)

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":

        # ensure symbol was submitted
        # ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("Provide symbol you must. Yes, hrrmmm.", 400)

        # ensure share was submitted
        elif not request.form.get("shares"):
            return apology("Provide shares you must. Yrsssss.", 400)

        # ensure share is valid number
        elif request.form.get("shares").isdigit() == False:
            return apology("Hrrmmm. Enter positive number you must. Hmm.", 400)

        # set variables
        user = get_current_user()
        symbol = request.form.get("symbol").upper()
        shares = int(request.form.get("shares"))
        balance = user["cash"]
        quote = get_quote(symbol)

        # get user share before selling out
        current_shares = get_user_share(symbol)

        # should be positive
        if shares < 0:
            return apology("Hrrmmm. Enter positive number you must. Hmm.", 400)

        # check for quote
        if quote is None:
            return apology("Has not found, quote.", 400)

        # check for insufficient share
        if shares > current_shares:
            return apology("Hrrrmmm. Not enough shares, you have.", 400)

        purchase_amount = int(shares) * quote["price"]

        # common method for handling transactions
        handle_transaction(balance, TransactionType.Sell.value,
                           symbol, shares, purchase_amount, quote["price"])

        # common method for updating stocks
        handle_current_stocks(
            symbol, quote["name"], TransactionType.Sell.value, shares)

        # if one share has 0 value it should be deleted from database
        if shares == current_shares:
            zero_share_job(symbol)

        return redirect("/")
    else:
        symbols = db.execute(
            "SELECT * FROM CurrentStocks where user_id = ?", session["user_id"])
        return render_template("sell.html", symbols=symbols)


# transaction types
class TransactionType(enum.Enum):
    Buy = 1
    Sell = 2

# get current user


def get_current_user():
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    return user[0]


# get quote with given symbol
def get_quote(symbol):
    quote = lookup(symbol)
    print(quote)
    if quote is None:
        return
    else:
        return quote

# insert transaction table and update user balance


def handle_transaction(balance, transaction_type, symbol, share, purchase_amount, price):
    now = datetime.datetime.now()
    transaction_query = "INSERT INTO Transactions (transaction_type, symbol, share, price, user_id ) VALUES(?,?,?,?,?)"
    db.execute(transaction_query, transaction_type,
               symbol, share, price, session["user_id"])

    new_balance = handle_balance(balance, purchase_amount, transaction_type)

    db.execute("UPDATE users SET cash = ? WHERE id = ?",
               new_balance, session["user_id"])

    return 0

# insert or update stocks on CurrentStocks table


def handle_current_stocks(symbol, name, transaction_type, share):
    exist_value = check_exist(symbol)
    if exist_value:
        prev_share = db.execute(
            "SELECT count FROM CurrentStocks WHERE symbol LIKE ? AND user_id = ?", symbol, session["user_id"])
        current_share = handle_shares(
            int(prev_share[0]['count']), int(share), transaction_type)
        db.execute("UPDATE CurrentStocks SET count = ? WHERE user_id = ? and symbol LIKE ?",
                   current_share, session["user_id"], symbol)
        return 0
    else:
        insert_query = "INSERT INTO CurrentStocks(symbol, name, count,user_id) VALUES(?,?,?,?)"
        db.execute(insert_query, symbol, name, share, session["user_id"])
        return 0


# handle calculations for shares
def handle_balance(balance, amount, transaction_type):
    new_balance = balance

    if transaction_type == 1:
        new_balance = new_balance - amount
    elif transaction_type == 2:
        new_balance = new_balance + amount

    print(new_balance)
    return new_balance

# handle calculations for shares


def handle_shares(total_share, share, transaction_type):
    new_share = total_share
    if transaction_type == 1:
        new_share = new_share + share
    elif transaction_type == 2:
        new_share = new_share - share
    print(new_share)
    return new_share

# check exist if user has the stock in his/her CurrentStocks


def check_exist(symbol):
    check_query = db.execute(
        "SELECT EXISTS(SELECT 1 FROM CurrentStocks WHERE symbol LIKE ? AND user_id = ? ) if_exist", symbol, session["user_id"])
    return check_query[0]['if_exist']


def get_user_share(symbol):
    exist = check_exist(symbol)
    if exist:
        prev_share = db.execute(
            "SELECT count FROM CurrentStocks WHERE symbol LIKE ? and user_id = ?", symbol, session["user_id"])
        return int(prev_share[0]['count'])
    else:
        return 0


# if a share has zero count on current stocks
# delete it from CurrentStocks table
def zero_share_job(symbol):
    db.execute("DELETE FROM CurrentStocks WHERE symbol LIKE ? AND user_id = ?",
               symbol, session["user_id"])
    return 0


# we keep the transaction types as Enum
# to have smaller data on database
# when UI receives the type
# this helper returns the value
# Buy or Sell
def visualize_transaction_type(type):
    if type == 1:
        return "Buy"
    else:
        return "Sell"
