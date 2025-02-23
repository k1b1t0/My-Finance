import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, vnd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["vnd"] = vnd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


def represents_int(s):
    try:
        int(s)
    except ValueError:
        return False
    else:
        return True


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
    funds = db.execute("SELECT name, amount FROM funds WHERE ID_user=?", session["user_id"])
    return render_template("index.html", funds=funds)


@app.route("/update", methods=["GET", "POST"])
@login_required
def update():
    if request.method == "GET":
        category = db.execute("SELECT name FROM categories")
        funds = db.execute("SELECT name FROM funds WHERE ID_user=?", session["user_id"])
        return render_template("update.html", category=category, funds=funds)
    else:
        amount = int(request.form.get("amount"))
        funds = request.form.get("funds")
        detail = request.form.get("detail")
        category = request.form.get("category")

        if not funds:
            return apology("must provide valid fund")
        if not category:
            return apology("must provide valid category")

        tmp = db.execute("SELECT id FROM categories WHERE name=?", category)
        id_category = int(tmp[0]["id"])

        # check neu so tien tieu nhieu hon so tien trong quy
        fund_money = db.execute(
            "SELECT amount, id FROM funds WHERE name=? AND ID_user=?", funds, session["user_id"])
        if (int(fund_money[0]["amount"]) + amount < 0):
            return apology("you don't have enough money to spend")

        # them giao dich vao purchases
        db.execute("INSERT INTO purchases(ID_user, amount, ID_ctg, detail, ID_fund) VALUES (?,?,?,?,?)",
                   session["user_id"], amount, id_category, detail, fund_money[0]["id"])
        # update tien trong fund
        db.execute("UPDATE funds SET amount=? WHERE id=?", int(
            fund_money[0]["amount"]) + amount, fund_money[0]["id"])
        return redirect("/")


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        check = db.execute("SELECT * FROM users WHERE username=?", username)
        if check:
            return apology("username is already taken")
        confirmation = request.form.get("confirmation")
        if not username or not password:
            return apology("must provide username and password")
        elif confirmation != password:
            return apology("wrong confirmation")
        db.execute("INSERT INTO users (username, hash) VALUES (?,?)",
                   username, generate_password_hash(password))
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/history")
@login_required
def history():
    infos = db.execute(
        "SELECT time, purchases.amount AS amount, detail, funds.name AS fund_name, categories.name AS category FROM purchases JOIN funds on funds.id = purchases.ID_fund JOIN categories on categories.id = purchases.ID_ctg WHERE purchases.ID_user=? ORDER BY time DESC", session["user_id"])
    return render_template("history.html", infos=infos)


@app.route("/addfund", methods=["GET", "POST"])
@login_required
def addfund():
    if request.method == "POST":
        name = request.form.get("name")
        check = db.execute("SELECT name FROM funds WHERE ID_user=? AND name=?",
                           session["user_id"], name)
        if check:
            return apology("fund is already existed")
        else:
            amount = int(request.form.get("amount"))
            db.execute("INSERT INTO funds (ID_user, name, amount) VALUES (?, ?, ?)",
                       session["user_id"], name, amount)
            return redirect("/")
    else:
        return render_template("addfund.html")
