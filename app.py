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

@app.route('/worker/get_announcement/<id>')
def get_announcement(id):
    return render_template('announcement.html',
                           announcement=Announcement.query.get_or_404(id)
                           )

@app.route('/worker/edit_announcement/<id>',  methods=['GET', 'POST'])
def edit_announcement(id):
    if request.method == 'POST':
        announcement = Announcement.query.get_or_404(id)
        announcement.id = request.form['id']
        announcement.title = request.form['title']
        announcement.description = request.form['description']
        announcement.date = date.today()
        announcement.readerVisibility = 'readerVisibility' in request.form
        db.session.commit()
        return redirect(url_for('worker'))
    return render_template('edit_announcement.html',
                           announcement=Announcement.query.get_or_404(id)
                           )

@app.route('/reader/get_all_reader_announcements')
def get_all_reader_announcements():
    return render_template('get_all_reader_announcements.html',
                           announcements=Announcement.query.order_by(Announcement.id.desc()).all()
                           )

@app.route('/worker/delete-announcement/<id>')
def delete_announcement(id):
    db.session.delete(Announcement.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('get_all_announcements'))

@app.route('/worker/update-announcement/<id>')
def update_announcement(id,Data):
    announcemt = Announcement.query.get_or_404(id)
    print(announcemt.data)
    print(Data)

    db.session.commit()
    return redirect(url_for('get_announcement/<id>'))

if __name__ == '__main__':
    app.run()
