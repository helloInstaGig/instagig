import os
from dotenv import load_dotenv
from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
load_dotenv()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Jobs(db.Model):
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50))
    name = db.Column(db.String(30))
    price = db.Column(db.Integer)
    comment = db.Column(db.Text())
    img = db.Column(db.LargeBinary)
    mimetype = db.Column(db.Text())
    timestamp = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    def __init__(self, title, name, price, comment, img, mimetype):
        self.title = title
        self.name = name
        self.price = price
        self.comment = comment
        self.img = img
        self.mimetype = mimetype


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/product")
def product():
    return render_template('product.html', title='Product')

@app.route("/contact")
def contact():
    return render_template('contact.html', title='Contact')

@app.route("/faq")
def faq():
    return render_template('faq.html', title='FAQ')

@app.route("/demo")
def demo():
    jobs = Jobs.query.filter().all()
    return render_template('demo.html', jobs=jobs)

@app.route("/delete", methods=['POST'])
def delete():
    if request.method == 'POST':
        db.drop_all()
        db.create_all()
        jobs = Jobs.query.filter().all()
        return render_template('demo.html', jobs=jobs)

@app.route("/submit", methods=['POST'])
def submit():
    if request.method == 'POST':

        title = request.form['title']
        name = request.form['name']
        comment = request.form['comment']
        price = request.form['price']
        img = request.files['image']
        mimetype = img.mimetype

        data = Jobs(title, name, price, comment, img.read(), mimetype)
        db.session.add(data)
        db.session.commit()
        jobs = Jobs.query.filter().all()
        return render_template('demo.html', jobs=jobs)

@app.route("/listing/<int:id>/thumbnail")
def thumbnail(id):
    thumbnail = Jobs.query.filter(Jobs.id == id)[0]
    return app.response_class(thumbnail.img, mimetype=thumbnail.mimetype)

