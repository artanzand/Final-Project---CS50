from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from datetime import date


# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///people.db")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/apology")
def apology():
    return render_template("apology.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via GET
    if request.method == "GET":
        return render_template("login.html")

    # User reached route via POST (as by submitting a form via POST)
    else:
        # Ensure name and id was submitted
        if not request.form.get("name"):
            return redirect("/apology")
        elif not request.form.get("id"):
            return redirect("/apology")


        # Query database for username
        rows = db.execute("SELECT * FROM people WHERE id=?", request.form.get("id"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or rows[0]["name"] != request.form.get("name"):
            return redirect("/apology")

        else:
            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]

            # Redirect user to home page
            return redirect("/self_assessment")



@app.route("/self_assessment")
def self_assessment():
    return render_template("self_assessment.html")


@app.route("/questionnaire", methods=["GET", "POST"])
def questionnaire():

    if request.method == "GET":
        return render_template("questionnaire.html")

    # User reached route via POST (as by submitting a form via POST)
    else:
        fever = request.form.get("fever")
        cough = request.form.get("cough")
        breath_short = request.form.get("breath_short")
        breath_diff = request.form.get("breath_diff")
        sore_throat = request.form.get("sore_throat")
        runny_nose = request.form.get("runny_nose")
        chills = request.form.get("chills")
        swallow = request.form.get("swallow")
        stuffy_nose = request.form.get("stuffy_nose")
        headache = request.form.get("headache")
        fatigue = request.form.get("fatigue")
        nausea = request.form.get("nausea")
        senses = request.form.get("senses")
        pink_eye = request.form.get("pink_eye")

        # load into symptoms table
        db.execute("INSERT INTO symptoms VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        session["user_id"], fever, cough, breath_short, breath_diff, sore_throat,
        runny_nose, chills, swallow, stuffy_nose, headache, fatigue, nausea, senses, pink_eye)

        # Redirect user to scheduling page
        return redirect("/schedule")


@app.route("/schedule", methods=["GET", "POST"])
def schedule():

    if request.method == "GET":
        # select five days from today and give to /schedule
        start_date = date.today()
        delta = datetime.timedelta(days=1)

        days=[]
        for i in range (0,5):
            days.append(start_date)
            start_date += delta

        return render_template("schedule.html", days=days)
    else:
        day = request.form.get("day")
        location = request.form.get("location")
        phone = request.form.get("phone")

        # updating a temp table
        reader = db.execute("SELECT * FROM temp WHERE user_id=?", session["user_id"])
        if len(reader) != 1:
            db.execute("INSERT INTO temp VALUES(?,?,?,?)", session["user_id"], location, day, phone)
        else:
            db.execute("UPDATE temp SET location=?, day=?, phone=? WHERE user_id=?", location, day, phone, session["user_id"])

        # Redirect user to scheduling page
        return redirect("/times")



@app.route("/times", methods=["GET", "POST"])
def times():
    temp = db.execute("SELECT * FROM temp WHERE user_id=?", session["user_id"])
    location = temp[0]["location"]
    day = temp[0]["day"]
    phone = temp[0]["phone"]

    if request.method == "GET":

        times = ["08:00", "08:30","09:00", "09:30","10:00", "10:30","11:00", "11:30","12:00", "12:30","13:00", "13:30","14:00", "14:30","15:00", "15:30"]
        rows = db.execute("SELECT time FROM tally WHERE location=? AND day=? AND count=3", location, day)

        for i in range(len(rows)):
            times.remove(rows[i]["time"])
        return render_template("times.html", times=times, location=location, day=day)

    # submit appointment
    else:
        ID = session["user_id"]
        time = request.form.get("time")
        hashed = generate_password_hash(str(ID))
        db.execute("INSERT INTO booked VALUES(?,?,?,?,?,?)", session["user_id"], hashed, location, day, time, phone)

        # updating the tally table
        reader = db.execute("SELECT count FROM tally WHERE location=? AND time=? AND day=?", location, time, day)
        if len(reader) != 1:
            db.execute("INSERT INTO tally VALUES(?,?,?,1)", location, time, day)
        
        else:
            count = int(reader[0]["count"])
            db.execute("UPDATE tally SET count=? WHERE location=? AND time=? AND day=? ", count+1, location, time, day)

        # Redirect user to home page
        return redirect("/success")


@app.route("/success")
def success():
    read = db.execute("SELECT hash FROM booked WHERE user_id=?", session["user_id"])
    hashed = read[0]["hash"]
    return render_template("success.html", hashed=hashed)
    

@app.route("/modify", methods=["GET", "POST"])
def modify():

    # User reached route via GET
    if request.method == "GET":
        return render_template("modify.html")

    # User reached route via selecting Cancel
    else:
        hashed = request.form.get("hash")
        action = request.form.get("action")
        reader = db.execute("SELECT user_id FROM booked WHERE hash=?", hashed)

        if len(reader) != 1:
            return redirect("/apology")

        # update tally table
        row = db.execute("SELECT * FROM booked WHERE hash=?", hashed)
        location = row[0]["location"]
        day = row[0]["day"]
        time = row[0]["time"]

        read = db.execute("SELECT count FROM tally WHERE location=? AND time=? AND day=?", location, time, day)
        count = int(read[0]["count"])
        db.execute("UPDATE tally SET count=? WHERE location=? AND time=? AND day=? ", count-1, location, time, day)

        # update booked table
        db.execute("DELETE FROM booked WHERE hash=?", hashed)

        # cancel appointment
        if action == "cancel":
            return redirect("/")

        # modify appointment
        else:
            session["user_id"] = reader[0]["user_id"]
            return redirect("/schedule")
