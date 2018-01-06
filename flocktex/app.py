import functools
import glob
import os
from os.path import join, dirname, relpath
import subprocess
import shutil
import sys

from flask import Flask
from flask import render_template
from flask_frozen import Freezer
from PIL import Image


app = Flask(__name__)
freezer = Freezer(app)

STATIC_FOLDER_PATH = join(dirname(__file__), 'static')

cover_images_path = list(map(lambda x: join('images', 'cover', x),
                             os.listdir(join(STATIC_FOLDER_PATH,
                                             'images',
                                             'cover'))))


BASE_TEMPLATE_VARS = {
    'usernames': {
        'facebook': 'FlockTexIn',
        'instagram': 'flocktexin',
        'linkedin': 'FlockTexIn',
        'twitter': 'FlockTexIn',
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
    prods = [
    {
        'name': 'FF-1216Y-2',
        'description': 'Machine with advance technology operating with double '
                       'head, each head working separately at the same time.',
        'features': [
            'High precision cutting, reducing wastage of material',
            'Fully automatic working reduce labour cost',
            'High accuracy cutting for material beyond format',
            'Smooth cutting edge with precised product quality',
            'Friendly interface',
            'Super high recognition',
        ],
        'applications': [
            {'name': 'Embroidery Patch',
             'img_name': 'embroidery_patch'},
            {'name': 'Embroidery Lace',
             'img_name': 'embroidery_lace'},
            {'name': 'Shoes Upper',
             'img_name': 'shoes_upper'},
            {'name': 'Undergarments / Lingerie',
             'img_name': 'undergarments_lingerie'},
            {'name': 'Double Layered Patch',
             'img_name': 'double_layered_patch'},
            {'name': 'Jacquard Lace',
             'img_name': 'jacquard_lace'},
        ],
        'specifications': {
            'Model No.': 'FF-1216Y-2',
            'Laser Head': 'Single / Double',
            'Laser': 'CO2 laser tube',
            'Cooling System': 'AC chiller',
            'Laser Tube Power': '80w, 100w, 130w, 150w',
            'Power Supply': 'AC220 ± 5% / 50Hz',
            'Cutting Deepness': '<= 10mm',
            'Dimensions': '2510 x 2160 x 2018.5mm (W x L x H)',
            'Working Area': '1600 x 1200mm (W x L)',
            'Weight': '± 1100 kg.',
        },
    },
    ]
    return render_template('products.html', prods=prods)


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


def build():
    # remove build dir if exists
    if os.path.exists(join(dirname(__file__), 'build')):
        shutil.rmtree(join(dirname(__file__), 'build'))

    # compress images
    globs = [
        '**/*.JPG',
        '**/*.jpg',
        '**/*.JPEG'
        '**/*.jpeg',
        '**/*.PNG',
        '**/*.png',
    ]
    globs = list(map(lambda x: join(dirname(__file__), 'static', 'images', x),
                     globs))

    image_files = []
    for path in globs:
        for file_path in glob.glob(path, recursive=True):
            image_files.append(os.path.abspath(file_path))

    for file in image_files:
        print("Compressing:", file)
        image = Image.open(file)
        if file.split('.')[-1] in ['jpg', 'jpeg', 'JPG', 'JPEG']:
            image.save(file, "JPEG", optimize=True, quality=85)

    # build
    freezer.freeze()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        build()
    else:
        app.run(debug=True)
