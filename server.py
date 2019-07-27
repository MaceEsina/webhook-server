from flask import Flask, request

PORT = 9000
app = Flask(__name__)

@app.route("/reminder-lesson", methods=['POST'])
def lesson():
    data = request.get_json()
    print(data)

if __name__ == "__main__":
    app.run(port=PORT)
