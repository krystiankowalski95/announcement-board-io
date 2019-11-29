import time

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///announcements.sqlite"
db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False)
    surname = db.Column(db.String, nullable=False)
    userType = db.Column(db.String,nullable=False)

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150),nullable=False)
    description = db.Column(db.String(500),nullable=False)
    date = db.Column(db.DateTime,nullable=False)
    readerVisibility = db.Column(db.Boolean,nullable=False)

    def __init__(self,id, title, description, dateAdded, readerVisibility):
        self.id = id
        self.title = title
        self.description = description
        self.date = dateAdded
        self.readerVisibility = readerVisibility

db.create_all()


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/reader')
def reader_page():
    return render_template("reader_main.html")

@app.route('/worker')
def worker_page():
    return render_template("worker_main.html")


@app.route('/worker_add_announcement')
def worker_add_announcement():
    return render_template("add_announcement.html")


@app.route('/worker_get_announcements')
def worker_get_announcements():
    return render_template("get_announcements.html")

@app.route('/reader_get_announcements')
def reader_get_announcements():
    return render_template("get_reader_announcements.html")


@app.route('/worker_add_announcement', methods=['GET', 'POST'])
def add_event():
    print(time.strftime('%A %B, %d %Y %H:%M:%S'))
    if request.method == 'POST':
        announcement = Announcement(id=request.form['id'], title=request.form['title'], description=request.form['description'],
                                    date=time.strftime('%A %B, %d %Y %H:%M:%S'),readerVisibility= request.form['readerVisibility'])
        db.session.add(announcement)
        db.session.commit()
        return redirect(url_for('worker_page'))
    return render_template('/worker',)

if __name__ == '__main__':
    app.run()
