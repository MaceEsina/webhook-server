from flask import Flask, request

PORT = 9000
app = Flask(__name__)

@app.route('/reminder-lesson', methods=['POST'])
def webhook():
    print('POST request')
    data = request.get_json()
    print('data:', data)
    return '', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)
