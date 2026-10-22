from flask import Flask, render_template, request
from datetime import datetime
import random


app = Flask(__name__)

app.secret_key = "topSecret"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/birds")
def birdPage():
    return render_template("bird.html")

@app.route("/seasons")
def seasonsPage():
    now = datetime.now()

    current_month = now.strftime("%B")

    current_Year = now.year

    return render_template("seasons.html",month =current_month,
                year=current_Year)

@app.route("/time")
def timePage():
    now = datetime.now()

    current_Hour = now.hour
    current_Minute = now.minute

    return render_template("time.html",hour=current_Hour,minute=current_Minute)

@app.route("/random")
def randomPage():
    randomNumber = random.randint(0,1000000)

    return render_template("random.html",number=randomNumber)

@app.route("/profile", methods=["GET","POST"])
def profilePage():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        quan = request.form.get("quan", "").strip()
        comments = request.form.get("comments", "").strip()
        rel = request.form.get("rel", "").strip()
        accommodations = request.form.get("accommodations") == "yes"

        if not name or not email or not quan or not rel:
            error = "Please fill in all required fields"
            return render_template("profileForm.html", error = error)
        return render_template("success.html", name = name, email=email, quan=quan, comments=comments, rel=rel, accommodations=accommodations)
    return render_template("profileForm.html")

@app.route("/feedback", methods=["GET", "POST"])
def feedbackPage():

    if request.method == "POST":
        rating = request.form.get("rating","").strip()
        feedback = request.form.get("feedback", "").strip()

        if not rating:
            error = "Please provide a rating"
            return render_template("feedbackForm.html", error=error)

        return render_template("feedbackSuccess.html", rating=rating, feedback=feedback)

    return render_template("feedbackForm.html")