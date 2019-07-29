from babel.dates import format_date
from datetime import date
from requests import post, get
from json import loads

def getToken():
  url = 'https://hwschool.s20.online/v2api/auth/login'
  params = {
    'email': 'magistresina@gmail.com',
    'api_key': '7de9c3ec-a931-11e9-9333-0cc47a6ca50e'
  }
  response = post(url, json=params)
  if response.status_code == 200:
    return loads(response.text)['token']

  print('Cannot get alfaCRM API token, error code:', response.status_code)
  print('Error text:', response.text)
  return False

def getCustomer(token, id):
  url = 'https://hwschool.s20.online/v2api/1/customer/update?id=' + str(id)
  headers = { 'X-ALFACRM-TOKEN': token }
  response = post(url, headers=headers)
  if response.status_code == 200:
    return loads(response.text)['model']
  return False

def sendMessage(customer, lesson):
  if not customer:
    return

  phoneStr = customer['phone'][0]
  phone = parsePhoneNumber(phoneStr)
  date = lesson['fields_new']['time_from']
  time = parseTime(date)
  day = parseDay(date)
  message = f'Напоминаем, что {day} в {time} по московскому времени у Вас запланирован урок. IT школа Hello world.'
  params = {
    'transport': 'whatsapp',
    'from': '79585802577',
    'to': '79111318607',
    'text': message
  }
  url = 'https://new62839487.wazzup24.com/api/v1.1/send_message'
  headers = { 'Authorization': 'b6f00c29a7a64927882dbf2e3386df48' }
  response = post(url, headers=headers, json=params)
  print('phone:', phone)
  print('message:', message)

  # send sms when the customer hasn't whatsapp
  if response.status_code != 201:
    url = 'https://sms.ru/sms/send'
    params = {
      'to': '79111318607',
      'msg': message,
      'api_id': 'D4837EA1-2B37-F238-D41F-12E7AA13E08B'
    }
    responseSMS = get(url, params=params)
    if responseSMS.status_code != 200:
      print('Error sms sending for customer with id', customer['id'])
      print('Error text:', responseSMS.text)

def parsePhoneNumber(str):
  return ''.join(i for i in str if i.isdigit())

def parseTime(str):
  return str.split(' ')[1][:-3]

def parseDay(str):
  dayStrArr = str.split(' ')[0].split('-')
  dayIntArr = list(map(int, dayStrArr))
  d = date(*dayIntArr)

  return format_date(d, 'd MMMM', locale='rus')
