from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/api/hello")
def hello():
    return jsonify({"message": "Hello, World!"})

@app.route("/api/greet/<name>")
def greet():
    name = "hi"
    return jsonify({"message": f"Hello, {name}!"})


if __name__ == "__main__":
    app.run(debug=True)

