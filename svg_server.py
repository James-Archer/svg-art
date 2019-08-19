from flask import Flask, jsonify, render_template, Markup, request
from flask_cors import CORS, cross_origin
import time
import json

import draw_lines as dl
from draw_diagonals import DiagonalArtist


def padZeros(num):
    if num < 10:
        return f"0{num}"
    else:
        return f"{num}"

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


class Server():

    def __init__(self):

        self.artists = {
            "Diagonals": DiagonalArtist(),
            "Another artist": DiagonalArtist()
        }
        self.currentArtist = None

    def setArtist(self, artist):

        self.currentArtist = artist

S = Server()


@app.route('/artists', methods=["GET"])
@cross_origin()
def send_artists():
    return jsonify([i for i in S.artists.keys()])


@app.route('/artist_inputs', methods=["POST"])
@cross_origin()
def send_artist_inputs():
    artist = S.artists[request.form['artist']]
    S.setArtist(artist)
    return jsonify(artist.inputs)


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
    width, height = int(request.form["width"]), int(request.form["height"])
    args = {}
    for key, val in request.form.items():
        if key not in ("width", "height"):
            k = key.replace("args[", "")
            k = k.replace("]", "")
            args[k] = val

    return S.currentArtist.RunInputs(min(width, height), **args)
    '''
    output = dl.make_maze(
        n,
        color=color,
        height=min(w, h),
        thickness=thickness)

    return output
    '''
    return
