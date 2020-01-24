from flask import Flask

secureApp = Flask(__name__)

@secureApp.route('/')
def index():
    return '<h1>Hey</h1>'
