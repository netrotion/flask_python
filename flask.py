from flask import Flask, render_template, request, flash, jsonify
import random
import time
from datetime import datetime
from threading import Thread
import urllib
import json
#pip install Flask Flask-SQLAlchemy


def selenthread():
  code = open('selen.py').read()
  exec(code)


app = Flask(__name__)
app.secret_key = 'supersecretkey'


#url = repl/getkey method = post, data = {'key':data}
#keymonttype = HNGL-MONTH-abcxyz, week tuong tu
#datajson = {data:{key1:[True,timegenerate],key2:[True,timegenerate]}}]}}
def random_string():
  s = 'QWERTYUIOPASDFGHJKLZXCVBNM1234567890'
  return ''.join(random.choice(s) for i in range(13))


def gk(k=None, typ=None):
  open('key_month', 'a')
  open('key_week', 'a')
  if k == None:
    month = {'data': {}}
    week = {'data': {}}
    for i in range(100):
      mon = f'HNGL-MONTH-{random_string()}'
      wek = f'HNGL-WEEK-{random_string()}'
      month['data'][mon] = ['true', time.time(),0]
      week['data'][wek] = ['true', time.time(),0]
    open('key_month', 'w').write(str(month))
    open('key_week', 'w').write(str(week))
  else:
    month = json.loads(open('key_month', 'r').read())
    week = json.loads(open('key_week', 'r').read())
    if typ == 'month':
      key = f'HNGL-MONTH-{random_string()}'
      del month['data'][k]
      month['data'][key] = ['true', time.time()]
    elif typ == 'week':
      key = f'HNGL-WEEK-{random_string()}'
      del week['data'][k]
      week['data'][key] = ['true', time.time()]
    open(f'key_month', 'w').write(str(month))
    open(f'key_week', 'w').write(str(week))
  return


#kiem tra key ngay,thang,tuan
def checkkey(data):
  try:
    kw = json.loads(open('key_week').read().replace("'",'"'))
    km = json.loads(open('key_month').read().replace("'",'"'))
  except Exception as e:
    gk()
    return checkkey(data)
  now = time.time()
  try:
    if 'MONTH' in data:
      time_lenght = now - km['data'][data][1]
    elif 'WEEK' in data:
      time_lenght = now - kw['data'][data][1]
    if time_lenght <= 604800 and 'WEEK' in data and bool(kw['data'][data][2]) == False:
      kw['data'][data][2] = 1
      open(f'key_week', 'w').write(str(kw))
      return [True, 'week']
    elif time_lenght <= 2592000 and 'MONTH' in data and bool(km['data'][data][2]) == False:
      km['data'][data][2] = 1
      open(f'key_month', 'w').write(str(km))
      return [True, 'month']
    elif 'WEEK' in data and time_lenght > 604800:
      return [False]
    elif 'MONTH' in data and time_lenght > 2592000:
      return [False]
  except  Exception as e:
    return [False]
  return [False]


@app.route('/getkey', methods=['POST'])
def check_route():
  try:
    data = request.get_json()
    check = checkkey(data['key'])
    if check[0]:
      response = {'status': True, 'message': 'Key hop le', 'type': check[1]}
    else:
      print('abc',check)
      response = {'status': False, 'message': 'key khong hop le hoac da duoc su dung'}
    return jsonify(response)
  except Exception as e:
    return jsonify({'status': False, 'message': "Dung mo api nua xin day."})


@app.route('/expires', methods=['POST'])
def expires():
  try:
    data = request.get_json()['key']
    try:
      if 'MONTH' in data:
        k = json.loads(open('key_month').read().replace("'",'"'))
      elif 'WEEK' in data:
        k = json.loads(open('key_week').read().replace("'",'"'))
      else:
        return jsonify({'status': False, 'message': 'Key khong hop le'})
      tn = k['data'][data][1]
      return jsonify({'status': True, 'message': str(tn)})
    except Exception as e:
      gk()
      return expires()
  except Exception as e:
    return jsonify({'status': False, 'message': "Dung mo api nua xin day."})





@app.route('/')
def catch_all():
  return render_template('menu.html')


@app.route('/hnglshop/key')
def key():
  return render_template('key.html')


@app.route('/<path:directory_name>')
def process_directory(directory_name):
  requested_path = request.path
  user_ip = request.headers.get('X-Forwarded-For',
                                request.remote_addr).split(',')[0]
  return render_template(
      'index.html', text_function=lambda: t_f_other(directory_name, user_ip))


def dec_key(s, ip):  #case1/case2
  ip = ip.replace('.', '')
  s = s.split('/')
  while '' in s:
    s.pop(s.index(''))
  c1, c2 = s[0], s[1]
  c1 = round(int(c1)**(1 / 1.48))
  c2 = round(((int(c2) / 3.14 / 2.01)**(1 / 11)) / datetime.now().month)
  print(c1, c2, '\n', ip, datetime.now().day)
  if int(ip) == int(c1) and int(c2) == int(datetime.now().day):
    return True
  return False


def generate_key(ip):
  t = time.time()
  key = f'HNGL-KEYN{datetime.now().day}-{int(int("".join(ip.split(".")))**1.48)}-{int((datetime.now().month*datetime.now().day)**11*3.14*2.01)}'
  return key


def check_syntax(direct):
  direct = direct.split('/')
  while '' in direct:
    direct.pop(direct.index(''))
  if len(direct) != 2:
    return False
  for i in direct:
    if not i.isalnum():
      return False
  return True


def t_f_other(direct, ip):
  try:
    if check_syntax(direct) and dec_key(direct, ip):
      text = generate_key(ip)
      return text
    else:
      return 'Wrong page directory'
  except ValueError:
    return 'Invalid IP'


if __name__ == '__main__':
  try:
    kw = json.loads(open('key_week').read().replace("'",'"'))
    km = json.loads(open('key_month').read().replace("'",'"'))
  except:
    gk()
  app.run(host="0.0.0.0", port=1111)
