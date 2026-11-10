from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
import random


app = Flask(__name__)

app.secret_key = "topSecret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guestlist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    quan = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.Text)
    rel = db.Column(db.String(50), nullable=False)
    accommodations = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

with app.app_context():
    db.create_all()




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


        try:
            new_profile = Profile(
                name=name,
                email=email,
                quan=int(quan),
                comments=comments,
                rel=rel,
                accommodations=accommodations
            )
            db.session.add(new_profile)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            error = "An error occured while saving your profile. Please try again"
            return render_template('profileForm.html', error=error)
        
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
        try:
            new_feedback = Feedback(
                rating=int(rating),
                comment=feedback
            )
            db.session.add(new_feedback)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            error = "An error occured while saving your feedback. Please try again."
            return render_template('feedbackForm.html', error=error)
        return render_template("feedbackSuccess.html", rating=rating, feedback=feedback)

    return render_template("feedbackForm.html")



@app.route('/admin/profiles')
def admin_profiles():
    profiles = Profile.query.all()
    return render_template('admin_profiles.html', profiles=profiles)

@app.route('/admin/feedback')
def admin_feedback():
    feedbacks = Feedback.query.all()
    return render_template('admin_feedback.html', feedbacks=feedbacks)

@app.route('/admin/profiles/appendComments', methods=("GET", "POST"))
def admin_profiles_appendComments():
    if request.method == "POST":
        text = request.form.get('append-text')
        rel_type = request.form.getlist('append-rel-selector')
        accom_type = request.form.getlist('append-accommodation-selector')

        if not text:
            error = "Please enter text"
            profiles = Profile.query.all()
            return render_template('admin_profiles.html', profiles=profiles, error=error)
        profiles_to_update = []

        if "all" in rel_type and "all" in accom_type:
            profiles_to_update = Profile.query.all()
        elif "all" in rel_type:
            for accom_type in accom_type:
                for profiles in Profile.query.filter_by(accommodations=accom_type).all():
                    profiles_to_update.append(profiles)
        elif "all" in accom_type:
            for rel_type in rel_type:
                for profiles in Profile.query.filter_by(rel=rel_type).all():
                    profiles_to_update.append(profiles)
        else:
            for rel_type in rel_type:
                for profiles in Profile.query.filter_by(rel=rel_type).filter_by(accommodations=accom_type).all():
                    profiles_to_update.append(profiles)

        for profile in profiles_to_update:
            profile.comments += "-" + text
        try:
            db.session.commit()
        except Exception as e:
            error = "Error adding text"
            profiles = Profile.query.all()
            return render_template('admin_profiles.html', profiles=profiles, error=error)
    try:
        profiles_to_update = Profile.query.filter_by(accommodations=True).all()
        for profile in profiles_to_update:
            if " - email accommodation form" not in profile.comments:
                profile.comments += " - email accommodation form"

        db.session.commit()
        return redirect(url_for('admin_profiles'))
    except Exception as e:
        db.session.rollback()
        error = f"Error updating profiles: {str(e)}"
        profiles = Profile.query.all()
        return render_template('admin_profiles.html', profiles=profiles, error=error)







@app.route('/quiz')
def quiz():
    return render_template('quiz.html')