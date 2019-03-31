from flask import Flask, request
from google.protobuf.json_format import MessageToJson 
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "/Users/ethanshedd/Downloads/credentials.json"

app = Flask(__name__)
@app.route("/")
def test():
    client = language.LanguageServiceClient()
    toAnalyze = request.values.get('text')
    document = types.Document(content = toAnalyze, type = enums.Document.Type.PLAIN_TEXT)
    result = client.analyze_entities(document = document)
    return MessageToJson(result)