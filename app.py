from flask import Flask, render_template
from datetime import datetime
import random

app = Flask(__name__)

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