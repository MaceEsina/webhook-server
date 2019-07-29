import requests
import json

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
  url = 'https://hwschool.s20.online/v2api/1/customer/update?id=' + str(id)
  headers = { 'X-ALFACRM-TOKEN': token }
  response = requests.post(url, headers=headers)
  if response.status_code == 200:
    return json.loads(response.text)['model']
  return False

def sendMessage(customer, lesson):
  if not customer:
    return

  # TODO delete
  return

  number = ''.join(i for i in customer['phone_number'][0] if i.isdigit())
  time = customer['time_from']
  message = f'Напоминаем, что сегодня в {time} по московскому времени у Вас запланирован урок. IT школа Hello world.'
  params = {
    'transport': 'whatsapp',
    'from': '79585802577',
    'to': '79111318607',
    'text': message
  }
  url = 'https://new62839487.wazzup24.com/api/v1.1/send_message'
  headers = { 'Authorization': 'b6f00c29a7a64927882dbf2e3386df48' }
  response = requests.post(url, headers=headers, json=params)

  # send sms when the customer hasn't whatsapp
  if response.status_code != 201:
    url = 'https://sms.ru/sms/send'
    params = {
      'to': '79111318607',
      'msg': message,
      'api_id': 'D4837EA1-2B37-F238-D41F-12E7AA13E08B'
    }
    responseSMS = requests.get(url, params=params)
    if responseSMS.status_code != 200:
      print('Error sms sending for customer with id', customer['id'])
      print('Error text:', responseSMS.text)
