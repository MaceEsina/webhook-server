from flask import Flask, request
from utils import getToken, getCustomer, sendMessage
import json

PORT = 9000
app = Flask(__name__)

@app.route('/reminder-lesson', methods=['POST'])
def webhook():
  data = request.get_json()
  print('Webhook data:', data)
  customerIds = data['fields_new']['customer_ids']

  for id in customerIds:
    token = getToken()
    if token:
      customer = getCustomer(token, id)
      sendMessage(customer, data)
      print('Customer info:', customer)

  return '', 200

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=PORT)
