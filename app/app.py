import random, time
from flask import Flask, request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUESTS = Counter(
    "app_http_requests_total", "Total HTTP requests",
    ["method", "endpoint", "status"],
)
LATENCY = Histogram(
    "app_request_duration_seconds", "Request latency in seconds",
    ["endpoint"],
)

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def record_metrics(response):
    if request.path != "/metrics":
        endpoint = request.url_rule.rule if request.url_rule else "unmatched"
        LATENCY.labels(endpoint).observe(time.time() - request.start_time)
        REQUESTS.labels(request.method, endpoint, response.status_code).inc()
    return response

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

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
