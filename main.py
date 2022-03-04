from flask import Flask, request, render_template, stream_with_context
from flask_assets import Environment, Bundle

import datetime
from pyphen import Pyphen
from vvspy import get_departures

app = Flask(__name__)
assets = Environment(app)
assets.register('css', Bundle(
    'css/*.scss', filters='pyscss,cssmin', output='screen.css'))

dic = Pyphen(lang='de_DE')
with open('config/buttons.csv') as file:
    dest_buttons = [line.rstrip().split(';') for line in file]


@app.template_filter()
def hypen(s):
    return dic.inserted(s, '&shy;')


@app.route("/")
@app.route("/dest/<dest_str>")
def hello_world(dest_str=None):
    limit = request.args.get('limit')
    limit = int(limit) if limit is not None and limit.isdigit() else 20

    def generate():
        yield render_template('header.html', dest_buttons=dest_buttons)
        deps = []
        for dest in (dest_str or "de:08111:6332,de:08111:6333").split(","):
            deps.extend(get_departures(dest, limit=limit))

        deps.sort(key=lambda dep: dep.real_datetime)
        yield render_template('content.html', deps=deps, now=datetime.datetime.now(),
                              dest_str=dest_str, limit=limit,
                              stop=deps[0].stop_name if len(deps) > 0 else None)
    return app.response_class(stream_with_context(generate()))
