import functools
import os
from os.path import join, dirname, relpath
import shutil
import sys

from flask import Flask
from flask import render_template
from flask_frozen import Freezer


app = Flask(__name__)
freezer = Freezer(app)

STATIC_FOLDER_PATH = join(dirname(__file__), 'static')

cover_images_path = list(map(lambda x: join('images', 'cover', x),
                             os.listdir(join(STATIC_FOLDER_PATH,
                                             'images',
                                             'cover'))))


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
                   'industry. ',
    'cover_images': cover_images_path,
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
    ignore = [
        '.gitignore'
    ]
    files = os.listdir(join(dirname(__file__),
                            'static/downloads'))
    return render_template('downloads.html', files=set(files) - set(ignore))


@app.route('/contact/')
def contact():
    template_vars = {
        'address': '3rd Floor, Plot No. 20, Mahesh Ind. Estate, Opp. Torrent '
                   'Power, Anjana Farm, Surat - 395003',
        'emails': [
            "info@flocktex.in",
        ],
        'phones': [
        {
            'number': '+91-99-30-991533',
            'name': 'Pragnesh Mangukiya',
        },
        {
            'number': '+91-98-19-642719',
            'name': 'Yatin Kapasi',
        },
        ],
    }

    return render_template('contact.html', **template_vars)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        try:
            shutil.rmtree(join(dirname(__file__), 'build'))
        except FileNotFoundError:
            # build dir doesn't exist; do nothing.
            pass
        finally:
            freezer.freeze()
    else:
        app.run(debug=True)
