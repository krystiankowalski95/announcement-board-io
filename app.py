from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///announcements.sqlite"
db = SQLAlchemy(app)

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150),nullable=False)
    description = db.Column(db.String(500),nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    readerVisibility = db.Column(db.Boolean)

    def __init__(self,id, title, description,date, readerVisibility):
        self.id = id
        self.title = title
        self.description = description
        self.date = date
        self.readerVisibility = readerVisibility

db.create_all()


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/reader')
def reader():
    return render_template("reader.html")

@app.route('/worker')
def worker():
    return render_template("worker.html")

@app.route('/worker/add_announcement', methods=['GET', 'POST'])
def add_announcement():
    if request.method == 'POST':
        announcement = Announcement(id=request.form['id'], title=request.form['title'], description=request.form['description'],
                                    date=date.today(),readerVisibility='readerVisibility' in request.form)
        db.session.add(announcement)
        db.session.commit()
        return redirect(url_for('worker'))
    return render_template('add_announcement.html',)

@app.route('/worker/get_announcements')
def get_announcements():
    return render_template('get_announcements.html',
                           announcements=Announcement.query.order_by(Announcement.id.desc()).all()
                           )

@app.route('/worker/get_all_announcements')
def get_all_announcements():
    return render_template('get_all_announcements.html',
                           announcements=Announcement.query.order_by(Announcement.id.desc()).all()
                           )

@app.route('/reader/get_all_reader_announcements')
def get_all_reader_announcements():
    return render_template('get_all_reader_announcements.html',
                           announcements=Announcement.query.order_by(Announcement.id.desc()).all()
                           )

if __name__ == '__main__':
    app.run()
