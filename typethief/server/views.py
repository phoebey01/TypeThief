# typethief/server/views.py

from flask import Flask


app = Flask(__name__)


@app.route('/newplayer')
def newplayer():
    pass


@app.route('/input/<id>')
def input(id):
    pass


@app.route('/empty/<id>')
def empty(id):
    pass
