import functools
import os
import shutil
import sys

from flask import Flask
from flask import render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer


app = Flask(__name__)
freezer = Freezer(app)


BASE_TEMPLATE_VARS = {
    'usernames': {
        'facebook': '',
        'instagram': '',
        'linkedin': '',
        'twitter': '',
        'github': 'flocktex',
    },
    'copyright_from_year': 2017,
    'copyright_to_year': 2018,
    'company_bio': 'Our company specializes in providing a high quality '
                   'laser cutting solution customized for the textile '
                   'industry. '
}


render_template = functools.partial(render_template, **BASE_TEMPLATE_VARS)


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
        try:
            shutil.rmtree(os.path.join(os.path.dirname(__file__), 'build'))
        except FileNotFoundError:
            # build dir doesn't exist; do nothing.
            pass
        finally:
            freezer.freeze()
    else:
        app.run(debug=True)
