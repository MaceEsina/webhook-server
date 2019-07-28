from flask import Flask, request
from utils import getToken, getCustomer, sendMessage

PORT = 9000
app = Flask(__name__)

@app.route('/reminder-lesson', methods=['POST'])
def webhook():
  response = request.get_json()
  customerIds = response['customer_ids']

  for id in customerIds:
    token = getToken()
    if token:
      customer = getCustomer(token, id)
      sendMessage(customer, response)
      print('Customer info:', customer)

  print('Webhook response data:', response)
  return '', 200

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=PORT)
