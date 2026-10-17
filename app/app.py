import random, time
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from the monitored app!"

@app.route("/slow")
def slow():
    time.sleep(random.uniform(0.5, 2.0))
    return "That was slow."

@app.route("/error")
def error():
    return "Something broke.", 500
