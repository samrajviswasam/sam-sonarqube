from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": "Hello from DevOps CI/CD Demo!",
        "status": "Application is running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/about")
def about():
    return jsonify({
        "application": "SonarQube Demo",
        "technology": "Python Flask",
        "purpose": "CI/CD and Kubernetes practice"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
