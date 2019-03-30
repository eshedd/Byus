from flask import Flask, render_template
app = Flask(__name__, static_url_path='')

import argparse

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


@app.route("/")
def hello():
    x = "mix.txt"
    text = ""
    with open(x, 'r') as f:
        for line in f.readlines():
            text += line.strip()
    return render_template('index.html', message=analyze(x), message2=(text)) 

def analyze(movie_review_filename):
    """Run a sentiment analysis request on text within a passed filename."""
    client = language.LanguageServiceClient()
    result = ""

    with open(movie_review_filename, 'r') as review_file:
        # Instantiates a plain text document.
        content = review_file.read()
    document = types.Document(
        content=content,
        type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document)

    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude

    if (score >= -0.25) & (score <= 0.25) & (magnitude >= 3):
        result += "This article seems neutral and gives a chance to both sides of the argument. We recommend it.\n"
    if (score >= -0.25) & (score <= 0.25) & (magnitude <= 3):
        result += "This article seems neutral but it seems to be unopinionated and doesn't include lots of information. We wouldn't recommend it.\n"
    if (score <= -0.25):
        result += "This article seems to take a negative stance on this topic and doesn't mention other sides of the argument. We recommend taking it with a pinch of salt.\n"
    if (score >= 0.25):
        result += "This article seems to take a positive stance on this topic and doesn't mention other sides of the argument. We recommend taking it with a pinch of salt.\n"
    
    #result += "( Score:" + str(score) + "\n"
    #result += "Magnitude:" + str(magnitude) + "\n)"
    return result
