from utils import getToken, getCustomer, sendMessage
from flask import Flask, request
from waitress import serve

PORT = 9000
app = Flask(__name__)

@app.route('/reminder-lesson', methods=['POST'])
def lessonWebhook():
  data = request.get_json()
  # print('Webhook data:', data)
  customerIds = data['fields_new']['customer_ids']

  for id in customerIds:
    token = getToken()
    if token:
      customer = getCustomer(token, id)
      sendMessage(customer, data)
      # print('Customer info:', customer)

  return '', 200

serve(app, host='0.0.0.0', port=PORT)
