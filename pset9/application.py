import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # execute database query
    rows = db.execute("SELECT symbol, SUM(shares) as totalShares FROM transactions WHERE user_id = '{user_id}' GROUP BY symbol HAVING totalShares > 0".format(
        **{"user_id": session["user_id"]}))

    holdings = []
    grand_total = 0
    for row in rows:
        stock = lookup(row["symbol"])
        holdings.append({
            "symbol": stock["symbol"],
            "name": stock["name"],
            "shares": row["totalShares"],
            "price": usd(stock["price"]),
            "total": usd(stock["price"] * row["totalShares"])
        })
        grand_total += stock["price"] * row["totalShares"]

    rows = db.execute("SELECT cash FROM users WHERE id = '{user_id}'".format(**{"user_id": session["user_id"]}))
    cash = rows[0]["cash"]
    grand_total += cash

    return render_template("index.html", holdings=holdings, cash=usd(cash), grand_total=usd(grand_total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        # extract stock symbol
        symbol = request.form.get("symbol")
        # extract shares
        shares = request.form.get("shares")

        # ensure name of stock and shares are submitted
        if not symbol or not shares:
            return apology("must provide stock symbol or shares")

        # check if a valid stock symbol is submitted
        buy = lookup(symbol)
        if not buy:
            return apology("stock symbol is not valid")

        # ensure shares is a positive integer
        if not shares.isdigit():
            return apology("enter a valid number")
        shares = int(shares)

        # buying process
        rows = db.execute("SELECT cash FROM users WHERE id = '{user_id}'".format(**{"user_id": session["user_id"]}))
        if not rows:
            return apology("Buying stock query failed")
        # check cash of user
        cash = rows[0]["cash"]
        share_cost = buy["price"] * shares
        if share_cost > cash:
            return apology("not enough cash!")
        else:
            updated_cash = db.execute(
                "UPDATE users SET cash = cash - '{share_cost}' WHERE id = '{user_id}'".format(**{"share_cost": share_cost, "user_id": session["user_id"]}))
            if not updated_cash:
                return apology("deducting cash query failed")
            buy_stock = db.execute("INSERT INTO transactions (user_id, symbol, shares, price) Values ('{user_id}', '{symbol}', '{shares}', '{price}')".format(
                **{"user_id": session["user_id"], "symbol": symbol, "shares": shares, "price": buy["price"]}))
            if not buy_stock:
                return apology("Buying stock query failed")
            flash("Successfully purchased {number} shares of {symbol}".format(**{"number": shares, "symbol": symbol}))
            return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # read transactions from database
    history = db.execute("SELECT symbol, shares, price, transacted FROM transactions WHERE user_id = '{user_id}' ORDER BY transacted desc".format(
        **{"user_id": session["user_id"]}))

    for transaction in history:
        transaction["price"] = usd(transaction["price"])
        transaction["transacted"] = transaction["transacted"]

    return render_template("history.html", history=history)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

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
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # extract stock symbol
        symbol = request.form.get("symbol")

        # ensure name of stock was submitted
        if not symbol:
            return apology("must provide stock symbol")

        # check if a valid stock symbol is submitted
        try:
            quote = lookup(symbol)
            quote["price"] = usd(quote["price"])
        except:
            # check if valid stock name is provided
            return apology("stock symbol is not valid")

        return render_template("quote_result.html", quote=quote)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not username:
            return apology("must provide username")

        # Ensure password was submitted
        elif not password:
            return apology("must provide password")

        # Ensure that password contains at least 8 characters
        # elif len(password) < 8:
        #    return apology("password is too short")

        # Ensure confirmation password was submitted
        elif not confirmation:
            return apology("must confirm password")

        # Ensure password and confirmation password are identical
        elif password != confirmation:
            return apology("passwords are not identical")

        # hash password
        hashPassword = generate_password_hash(password)

        try:
            # add user to database and check uniqueness of username
            result = db.execute("INSERT INTO users (username, hash) Values ('{username}', '{hash}')".format(
                **{"username": username, "hash": hashPassword}))
        except:
            return apology("username already exists")

        # log them in
        rows = db.execute("SELECT id FROM users WHERE username = '{username}'".format(**{"username": username}))
        if not rows:
            return apology("Query failed")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        # extract stock symbol
        symbol = request.form.get("symbol")
        # extract shares
        shares = request.form.get("shares")

        # ensure name of stock and shares are submitted
        if not symbol or not shares:
            return apology("must provide stock symbol or shares")

        # check if a valid stock symbol is submitted
        try:
            sell = lookup(symbol)
        except:
            # check if valid stock name is provided
            return apology("stock symbol is not valid")

        # ensure shares is a positive integer
        if not shares.isdigit():
            return apology("enter a valid number")
        # transform shares into an integer
        shares = int(shares)

        # check if user has entered a symbol he/she owns and that there are enough shares to sell
        rows = db.execute("SELECT symbol, SUM(shares) as totalShares FROM transactions WHERE user_id = '{user_id}' GROUP BY symbol HAVING totalShares > 0".format(
            **{"user_id": session["user_id"]}))
        for row in rows:
            if row["symbol"] == symbol:
                if shares > row["totalShares"]:
                    return apology("Not enough shares to sell")

        # make it negative to indicate that the user wants to sell shares
        shares = 0 - shares

        # selling process
        # calculate total price of shares
        share_cost = sell["price"] * shares

        updated_cash = db.execute("UPDATE users SET cash = cash - '{share_cost}' WHERE id = '{user_id}'".format(
            **{"share_cost": share_cost, "user_id": session["user_id"]}))  # - instead + because of negative costs
        if not updated_cash:
            return apology("deducting cash query failed")
        sell_stock = db.execute("INSERT INTO transactions (user_id, symbol, shares, price) Values ('{user_id}', '{symbol}', '{shares}', '{price}')".format(
            **{"user_id": session["user_id"], "symbol": symbol, "shares": shares, "price": sell["price"]}))
        if not sell_stock:
            return apology("selling stock query failed")

        flash("Successfully sold {number} shares of {symbol}".format(**{"number": shares, "symbol": symbol}))
        return redirect("/")

    else:
        rows = db.execute("SELECT symbol FROM transactions WHERE user_id = '{user_id}' GROUP BY symbol HAVING SUM(shares) > 0".format(
            **{"user_id": session["user_id"]}))
        return render_template("sell.html", symbols=[row["symbol"] for row in rows])


@app.route("/changePassword", methods=["GET", "POST"])
@login_required
def changePassword():
    """Change Password"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure password was submitted
        if not password:
            return apology("must provide password")

        # Ensure that password contains at least 8 characters
        # elif len(password) < 8:
        #    return apology("password is too short")

        # Ensure confirmation password was submitted
        elif not confirmation:
            return apology("must confirm password")

        # Ensure password and confirmation password are identical
        elif password != confirmation:
            return apology("passwords are not identical")

        # hash password
        hashPassword = generate_password_hash(password)

        # update password
        success = db.execute("UPDATE users SET hash = '{hashPassword}' WHERE id = '{user_id}'".format(
            **{"hashPassword": hashPassword, "user_id": session["user_id"]}))
        if not success:
            return apology('Database update failed')

        flash('Password successfully changed!')
        # redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("changePassword.html")


@app.route("/addCash", methods=["GET", "POST"])
@login_required
def addCash():
    """add Cash"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        amount = request.form.get("amount")

        # Ensure amount was submitted
        if not amount:
            return apology("must provide amount")

        # ensure amount is a positive integer
        if not amount.isdigit():
            return apology("enter a valid number")
        amount = int(amount)

        # update cash
        success = db.execute(
            "UPDATE users SET cash = cash + '{amount}' WHERE id = '{user_id}'".format(**{"amount": amount, "user_id": session["user_id"]}))
        if not success:
            return apology('Database update failed')

        flash('Successfully added cash!')
        # redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("addCash.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
