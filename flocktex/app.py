import functools
import glob
import os
from os.path import join, dirname, relpath
from pathlib import Path
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
        'youtube': 'UC91TwqcStpfGgwZAL7XMdKg',
    },
    'copyright_from_year': 2017,
    'copyright_to_year': 2018,
    'company_bio': 'Our company specializes in providing a high quality '
                   'laser cutting solution customized for the textile '
                   'industry. ',
    'cover_images': cover_images_path,
}

SURAT_ADDRESS = ('3rd Floor, Plot No. 20, Mahesh Ind. Estate, Opp. Torrent '
                 'Power, Anjana Farm, Surat - 395003')
SOUTH_ADDRESS = ('12/87a, KRG Nagar Back Side, Kallappachi Street, '
                 'Rakkiyapalayam, Avinashi Taluk, Tiruppur')


QRs = {
    'pragnesh': {
        'name': 'Pragnesh Mangukiya',
        'phone': '+91-99-30-991533',
        'email': 'info@flocktex.in',
        'address': ADDRESS,
    },
    'yatin': {
        'name': 'Yatin Kapasi',
        'phone': '+91-98-19-642719',
        'email': 'info@flocktex.in',
        'address': ADDRESS,
    },
    'sanjay': {
        'name': 'Sanjay Dankhara',
        'phone': '+91-98-20-233382',
        'email': 'info@flocktex.in',
        'address': ADDRESS,
    },
    'anand': {
        'name': 'P. Anandhakumar',
        'phone': '+91-96-29-077780',
        'email': 'info@flocktex.in',
        'address': SOUTH_ADDRESS,
    },
}


render_template = functools.partial(render_template, **BASE_TEMPLATE_VARS)


@freezer.register_generator
def qr_url_generator():
    for endpoint in QRs.keys():
        yield 'qr', {'name': endpoint}


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
        'name': 'Falcon',
        'model': 'FF-1216Y-2',
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
        'addresses': [
            SURAT_ADDRESS,
            SOUTH_ADDRESS,
        ],
        'emails': [
            "info@flocktex.in",
        ],
        'phones': [
            {
                'number': QRs['pragnesh']['phone'],
                'name': QRs['pragnesh']['name'],
            },
            {
                'number': QRs['yatin']['phone'],
                'name': QRs['yatin']['name'],
            },
            {
                'number': QRs['anand']['phone'],
                'name': QRs['anand']['name'],
            },
        ],
    }

    return render_template('contact.html', **template_vars)


@app.route('/qr/<name>/')
def qr(name):
    return render_template('qr.html', **QRs[name])


@app.route('/videos/')
def videos():
    video_ids = [
        'BHzoEmrEbTw',
        'TZJaYwUZ3To',
        'CQ2mwjU0tnE',
        '1pH8ogJCPRc',
    ]
    return render_template('videos.html', video_ids=video_ids)


def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def build(optimize=False):
    # remove build dir if exists
    if os.path.exists(join(dirname(__file__), 'build')):
        shutil.rmtree(join(dirname(__file__), 'build'))

    # compress images
    if optimize:
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
            image = Image.open(file)
            if file.split('.')[-1] in ['jpg', 'jpeg', 'JPG', 'JPEG']:
                old_size = os.path.getsize(file)
                image.save(Path(file), "JPEG", optimize=True, quality=60)
                new_size = os.path.getsize(file)
                print(file, "compressed from", sizeof_fmt(old_size), "to",
                      sizeof_fmt(new_size))

    # build
    freezer.freeze()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        optimize = '-opt' in sys.argv
        build(optimize)
    else:
        app.run(debug=True)
