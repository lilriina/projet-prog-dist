from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/titre")
def titre():
    # Simple fixed message
    return jsonify({"titre": "Have a nice day!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)