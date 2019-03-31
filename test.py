from flask import Flask, request, send_file
from google.protobuf.json_format import MessageToJson 
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "/Users/ethanshedd/Downloads/credentials.json"

app = Flask(__name__)#static_url_path='/Users/ethanshedd/Documents/GitHub/Byus-chrome-extension/')
@app.route("/")
def home():
    return send_file('popup.html')
#    return render_template('popup.html')
@app.route("/analyze")
def test():
    client = language.LanguageServiceClient()
    toAnalyze = request.values.get('text')
    document = types.Document(content = toAnalyze, type = enums.Document.Type.PLAIN_TEXT)
    result = client.analyze_entities(document = document)
    return MessageToJson(result)