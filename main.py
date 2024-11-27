from flask import Flask, jsonify, request
from api.MangaApiClient import MangaApiClient

app = Flask(__name__)

@app.route('/manga/<string:title>', methods=['GET'])
def getMangaName(title):
    return MangaApiClient.getManga(title)

@app.route('/manga-list/<string:id>', methods=['GET'])
def getMangaList(id):
    return MangaApiClient.getMangaList(id)

@app.route('/manga-pages/<string:id>')
def getMangasPages(id):
    return MangaApiClient.getMangasPages(id)

app.run(port=5000, host='localhost', debug=True)