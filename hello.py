from flask import Flask, jsonify, render_template, Markup, request
from flask_cors import CORS, cross_origin
import time

import draw_lines as dl

def padZeros(num):
    if num < 10:
        return f"0{num}"
    else:
        return f"{num}"

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello_world():
    return 'Flask text!'

@app.route('/getstuff', methods=["GET"])
@cross_origin()
def get_stuff():
    current_time = time.localtime()
    hrs, mins = current_time[3], current_time[4]
    return f"Some flasky words! @ {padZeros(hrs)}:{padZeros(mins)}"

@app.route('/get.svg', methods=["GET"])
@cross_origin()
def get_svg():
    svg = "".join([i for i in open('lines.svg')])
    return svg

@app.route('/sendprops', methods=["POST"])
@cross_origin()
def generate_svg():
    w, h, n = int(request.form['width']), int(request.form['height']), int(request.form['n'])
    color = request.form['color']
    thickness = int(request.form['thickness'])
    output = dl.make_maze(n, color=color, height=min(w, h), thickness=thickness)

    return output