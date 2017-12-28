import sys

from flask import Flask
from flask import render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer


app = Flask(__name__)
freezer = Freezer(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/products/')
def products():
    return render_template('products.html')


@app.route('/downloads/')
def downloads():
    return render_template('downloads.html')


@app.route('/contact/')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        freezer.freeze()
    else:
        app.run(debug=True)
