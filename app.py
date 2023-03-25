import re

from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from cs50 import SQL
import os

from helper import login_required, category_check
from datetime import date

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

UPLOAD_FOLDER = "./static/profilePictures"
ALLOWED_EXTENSIONS = {".jpg", ".png", ".jpeg", ".webp"}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

Session(app)

db = SQL("sqlite:///finalproject.db")

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

    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    user_money = db.execute("SELECT money FROM users WHERE id = ?", session["user_id"])
    history = db.execute("SELECT date, amount, category, type, desc FROM history WHERE user_id = ? ORDER BY date", session["user_id"])[-10:]
    date = []
    amount = []
    category = []
    type = []
    desc = []
    count = 0

    for i in range(len(history)):
        date.append(history[i]["date"])
        amount.append(history[i]["amount"])
        category.append(history[i]["category"].replace('_', ' ').title())
        type.append(history[i]["type"])

        dsc = history[i]["desc"]

        if dsc == None:
            dsc = "-"
        desc.append(dsc.title())

        count = count + 1

    expenses = db.execute("SELECT expense, category FROM expenses WHERE user_id = ? ORDER BY expense DESC LIMIT 3", session["user_id"])

    x = []
    for i in range(len(expenses)):
        top = {}
        top["expense"] = expenses[i]["expense"]
        top["category"] = expenses[i]["category"]
        icon_code = category_check(top["category"])
        top["code"] = icon_code
        x.append(top)

    if len(expenses) != 3:
        for i in range(3 - len(expenses)):
            top = {}
            top["expense"] = 0
            top["category"] = "-"
            top["code"] = "fa-solid fa-question"
            x.append(top)

    profPicPath = "basicProfile.png"
    files = os.listdir('./static/profilePictures')
    for f in files:
        if username in str(f):
            profPicPath = f"{str(f)}"
            break


    return render_template("index.html", money=user_money[0]["money"], date=date[::-1], amount=amount[::-1], category=category[::-1], type=type[::-1], desc=desc[::-1], count=count, onetwothree=x, username=username, picPath=profPicPath)

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    #user reaches page via POST
    if request.method == "POST":
        #ensure proper input
        #ensure user filled username

        username = request.form.get("username")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if rows == None:
            return render_template("fail_log.html")

        #ensure user filled password
        password = request.form.get("password")
        if not password:
            return render_template("fail_log.html")

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("fail_log.html")

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not username:
            return render_template("fail_reg.html", username=username, error="Please enter username!")

        elif not password:
            return render_template("fail_reg.html", username=username, error="Please enter password")

        elif not confirmation:
            return render_template("fail_reg.html", username=username, error="Please enter confirmation")

        elif password != confirmation:
            return render_template("fail_reg.html", username=username, error="Passwords do not match!")

        try:
            user_id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))
        except:
            return render_template("fail_reg.html", username=username, error="Username taken!")

        session["user_id"] = user_id

        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/income", methods=["GET", "POST"])
@login_required
def income():
    if request.method == "POST":
        amount = request.form.get("amount")
        desc = request.form.get("description")
        date_ = request.form.get("date")
        category = request.form.get("category")

        if not amount:
            return redirect("/")
        elif not category:
            return redirect("/")
        try:
            isInt = int(amount)
        except:
            return redirect("/")

        amount = float(amount)
        if amount < 0:
            return redirect("/")

        if len(date_) == 0:
            date_ = date.today()

        if len(db.execute("SELECT category FROM income_ WHERE category = ? AND user_id = ?", category, session["user_id"])) == 0:
            db.execute("INSERT INTO income_ VALUES(?, ?, ?, ?)", session["user_id"], amount, category, desc)
        else:
            old_amount = db.execute("SELECT income FROM income_ WHERE category = ? AND user_id = ?", category, session["user_id"])
            new_amount = old_amount[0]["income"] + amount
            db.execute("UPDATE income_ SET income = ? WHERE user_id = ? AND category = ?", new_amount, session["user_id"], category)

        cash = db.execute("SELECT money FROM users WHERE id = ?", session["user_id"])
        db.execute("UPDATE users SET money = ? WHERE id = ?", cash[0]["money"] + amount, session["user_id"])
        db.execute("INSERT INTO history VALUES(?, ?, ?, ?, ?, ?)", session["user_id"], amount, category, "in", desc, date_)
        return redirect("/")
    else:
        return redirect("/")

@app.route("/expense", methods=["GET", "POST"])
@login_required
def expense():
    if request.method == "POST":
        amount = request.form.get("amount")
        desc = request.form.get("description")
        date_ = request.form.get("date")
        category = request.form.get("category")

        if not amount:
            return redirect("/")
        elif not category:
            return redirect("/")
        try:
            isInt = int(amount)
        except:
            return redirect("/")

        amount = float(amount)
        if amount < 0:
            return redirect("/")

        if len(date_) == 0:
            date_ = date.today()

        cash = db.execute("SELECT money FROM users WHERE id = ?", session["user_id"])
        if amount > cash[0]["money"]:
            return redirect("/")

        if len(db.execute("SELECT category FROM expenses WHERE category = ? AND user_id = ?", category, session["user_id"])) == 0:
            db.execute("INSERT INTO expenses VALUES(?, ?, ?, ?)", session["user_id"], amount, category, desc)
        else:
            old_amount = db.execute("SELECT expense FROM expenses WHERE category = ? AND user_id = ?", category, session["user_id"])
            new_amount = old_amount[0]["expense"] + amount
            db.execute("UPDATE expenses SET expense = ? WHERE user_id = ? AND category = ?", new_amount, session["user_id"], category)

        db.execute("UPDATE users SET money = ? WHERE id = ?", cash[0]["money"] - amount, session["user_id"])
        db.execute("INSERT INTO history VALUES(?, ?, ?, ?, ?, ?)", session["user_id"], amount, category, "out", desc, date_)
        return redirect("/")
    else:
        return redirect("/")

@app.route("/user")
@login_required
def user():
    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]['username']
    expenses = db.execute("SELECT expense FROM expenses WHERE user_id = ?", session["user_id"])
    incomes = db.execute("SELECT income FROM income_ WHERE user_id = ?", session["user_id"])

    countIn = int(db.execute("SELECT COUNT(income) FROM income_ WHERE user_id = ?", session["user_id"])[0]['COUNT(income)'])
    countEx = int(db.execute("SELECT COUNT(expense) FROM expenses WHERE user_id = ?", session["user_id"])[0]['COUNT(expense)'])

    history = db.execute("SELECT date, amount, category, type, desc FROM history WHERE user_id = ?", session["user_id"])

    date = []
    amount = []
    category = []
    type = []
    desc = []
    count = 0

    for i in range(len(history)):
        date.append(history[i]["date"])
        amount.append(history[i]["amount"])
        category.append(history[i]["category"].replace('_', ' ').title())
        type.append(history[i]["type"])

        dsc = history[i]["desc"]

        if dsc == None:
            dsc = "-"
        desc.append(dsc.title())

        count = count + 1

    totalExpenses = sum([int(a['expense']) for a in expenses])
    totalIncome = sum([int(a['income']) for a in incomes])

    profPicPath = "basicProfile.png"
    files = os.listdir('./static/profilePictures')

    for f in files:
        if username in str(f):
            profPicPath = f"{str(f)}"
            break

    return render_template("user.html", username=username, totalExpenses=totalExpenses, totalIncome=totalIncome, totalTransactions=countIn+countEx, date=date[::-1], amount=amount[::-1], category=category[::-1], type=type[::-1], desc=desc[::-1], count=count, picPath=profPicPath)

@app.route("/calendar")
@login_required
def calendar():
    return render_template("calendar.html")

@app.route("/delete", methods=["GET", "POST"])
@login_required
def deleteTransaction():
    if request.method == "POST":
        db.execute("DELETE FROM history WHERE user_id = ?", session["user_id"])
        db.execute("DELETE FROM expenses WHERE user_id = ?", session["user_id"])
        db.execute("DELETE FROM income_ WHERE user_id = ?", session["user_id"])
        db.execute("UPDATE users SET money = 0 WHERE id = ?", session["user_id"])
        return redirect("/user")
    else:
        return redirect("/user")

@app.route("/lookup")
@login_required
def lookup():
    q = request.args.get("q")
    if q:
        transactions = db.execute("SELECT * FROM history WHERE date = ? AND user_id = ?", request.args.get("q"), session["user_id"])
    else:
        transactions = []
    return jsonify(transactions)

def allowed_file(filename):
    return '.' in filename and filename.split('.')[1].lower() in ALLOWED_EXTENSIONS

@app.route("/profilePic", methods=["GET", "POST"])
@login_required
def profilePic():
    if request.method == "POST":
        if 'file' not in request.files:
            print("assu")
            return redirect("/user")
        file = request.files['file']
        if file.filename == '':
            print("assu")
            return redirect("/user")

        # and allowed_file(file.filename)
        if file:
            print("assu")
            files = os.listdir("./static/profilePictures")
            username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]['username']
            for f in files:
                if username in str(f):
                    os.remove(f'./static/profilePictures/{f}')
                    break

            file.filename = f"{username}.{file.filename.split('.')[1].lower()}"
            print(file.filename)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect("/user")
    else:
        return redirect("/user")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/")