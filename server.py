from flask import Flask, request
import requests
import json

PORT = 9000
app = Flask(__name__)

def sendWhatsappMessage(data):
  if not data:
    return

  params = {
    'transport': 'whatsapp',
    'from': '79585802577',
    'to': '79111318607',
    'text': 'тестовое соощение whatsapp'
  }
  url = 'https://new62839487.wazzup24.com/api/v1.1/send_message'
  headers = { 'Authorization': 'b6f00c29a7a64927882dbf2e3386df48' }
  response = requests.post(url, headers=headers, json=params)
  print('resp whatsapp', response.text)

  # TODO replace == to !=
  if response.status_code == 201:
    sendSMS(data)

def sendSMS(data):
  url = 'https://sms.ru/sms/send'
  params = {
    'to': '79111318607',
    'msg': 'тестовое сообщение sms',
    'api_id': 'D4837EA1-2B37-F238-D41F-12E7AA13E08B'
  }
  response = requests.post(url, json=params)
  # TODO if response.status_code == 100
  print('resp sms', response.text)

def getToken():
  url = 'https://hwschool.s20.online/v2api/auth/login'
  params = {
    'email': 'magistresina@gmail.com',
    'api_key': '7de9c3ec-a931-11e9-9333-0cc47a6ca50e'
  }
  response = requests.post(url, json=params)
  if response.status_code == 200:
    return json.loads(response.text)['token']

  print('Cannot get alfaCRM API token, error code:', response.status_code)
  print('Error text:', response.text)
  return False

def getCustomer(token, id):
  url = 'https://hwschool.s20.online/v2api/1/customer/update?id=1857'
  headers = { 'X-ALFACRM-TOKEN': token }
  response = requests.post(url, headers=headers)
  if response.status_code == 200:
    return json.loads(response.text)['model']
  return False

@app.route('/reminder-lesson', methods=['POST'])
def webhook():
  webhookData = request.get_json()
  customerIds = json.loads(response.text)['customer_ids']
  print('POST response data:', webhookData)

  for id in customerIds:
    token = getToken()
    if token:
      customer = getCustomer(token, id)
      print('customer info:' customer)
      print('customer phone:', customer['phone'])
      sendWhatsappMessage(customer)

  return '', 200

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=PORT)
