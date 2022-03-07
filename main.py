from flask import Flask, request, render_template, stream_with_context, send_file
from flask_assets import Environment, Bundle

import datetime
import hashlib
import os
from pyphen import Pyphen
from vvspy import get_departures


def hashreplace(_in, out, **kw):
    # compute hash for sw based on main.py, css hash, environment and buttons
    hash = hashlib.md5()
    hash.update(bundleCSS.get_version().encode('utf-8'))
    hash.update(os.environ.get('VVS_BUTTONS', '').encode('utf-8'))
    for filename in os.listdir('templates'):
        with open('templates/' + filename, 'rb') as f:
            hash.update(f.read())
    with open('main.py', 'rb') as f:
        hash.update(f.read())

    out.write(_in.read()
              .replace('CSS_HASH', bundleCSS.get_version())
              .replace('SW_HASH', hash.hexdigest()[0:6]))


app = Flask(__name__)
assets = Environment(app)

bundleCSS = assets.register('css', Bundle(
    'css/*.scss', filters='pyscss,cssmin', output='screen.css'))
bundleCSS.build()
assets.register('sw', Bundle('sw.js', filters=hashreplace,
                depends='css/*.scss', output='sw.min.js')).build()  # but also depends on templates

dic = Pyphen(lang='de_DE')
dest_buttons = [line.strip().split(';')
                for line in os.environ.get('VVS_BUTTONS', '').splitlines()]


@app.template_filter()
def hypen(s):
    return dic.inserted(s, '&shy;')


@app.template_filter()
def joinDE(l):
    if len(l) == 1:
        return l[0]
    return ', '.join(l[:-1]) + ' und ' + l[-1]


@app.route("/")
@app.route("/dest/<dest_str>")
def hello_world(dest_str=None):
    def generate():
        yield render_template('header.html', dest_buttons=dest_buttons)
        yield content(dest_str=dest_str)
    return app.response_class(stream_with_context(generate()))


@app.route("/content/<dest_str>")
def content(dest_str=None):
    limit = request.args.get('limit')
    limit = int(limit) if limit is not None and limit.isdigit() else 20

    deps = []
    for dest in (dest_str or "de:08111:6332,de:08111:6333").split(","):
        deps.extend(get_departures(dest, limit=limit))

    deps.sort(key=lambda dep: dep.real_datetime)
    return render_template('content.html', deps=deps, now=datetime.datetime.now(),
                           dest_str=dest_str, limit=limit,
                           stops=sorted(set([dep.stop_name for dep in deps])))


@app.route("/header")
def header():
    return render_template('header.html', dest_buttons=dest_buttons)


@app.route("/offline")
def offline():
    return render_template('offline.html')


@app.route("/sw.js")
def sw():
    return send_file('static/sw.min.js')
