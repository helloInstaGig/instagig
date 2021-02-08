from flask import Flask, render_template, url_for
app = Flask(__name__)

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









