from flask import Flask, jsonify, request
from api.CreateFile import CreateFile
from api.MangaApiClient import MangaApiClient

app = Flask(__name__)

@app.route('/manga/<string:title>', methods=['GET'])
def getMangaName(title):
    return MangaApiClient.getManga(title)

@app.route('/manga-list/<string:id>', methods=['GET'])
def getMangaList(id):
    return MangaApiClient.getMangaList(id)

@app.route('/manga-pages/<string:id>', methods=['GET'])
def getMangasPages(id):
    return MangaApiClient.getMangasPages(id)

@app.route('/download-files/<path:manga_path>', methods=['POST'])
def pasteCreate(manga_path):
    return CreateFile.pasteCreate(manga_path)

@app.route('/download-pdf/<path:manga_path>', methods=['POST'])
def pdfGenerator(manga_path):
    return CreateFile.pdfGenerator(manga_path)

@app.route('/download-mobi/<path:manga_path>', methods=['POST'])
def mobiGenerator(manga_path):
    return CreateFile.mobiGenerator(manga_path)

app.run(port=5000, host='localhost', debug=True)