from flask import Flask, render_template, request, flash
import random
import time
from datetime import datetime
from threading import Thread
import urllib



app = Flask(__name__)
app.secret_key = 'supersecretkey'


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
  print(c1, c2,'\n',ip,datetime.now().day)
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


def uptime():
  while True:
    time.sleep(5)
    try:
       urllib.request.urlopen('https://9625587c-c04c-4b41-8364-bdf01c8a66bb-00-1p5hk1g7p7jia.sisko.replit.dev/')
    except:pass

if __name__ == '__main__':
  uptime_thread = Thread(target=uptime)
  uptime_thread.start()

  app.run(host="0.0.0.0", port=random.randint(2000, 9000))
