import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_mail import Mail, Message
from bs4 import BeautifulSoup
import requests
import html5lib
import sys
#import re

app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ritts.1997@gmail.com'
app.config['MAIL_PASSWORD'] = '1234Abcd'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_SUPRESS_SEND'] = False
app.config['DEBUG'] = True
app.config['MAIL_DEBUG'] = True
app.config['TESTING'] = False
mail = Mail(app)
url1 = 'https://www.mscwb.org/home/emp_notice'
url2 = 'https://www.mscwb.org/home/results'
#url1 = '/home/ritts97/Projects/test1.html'
#url2 = '/home/ritts97/Projects/test2.html'

scheduler = BackgroundScheduler()

content1 = BeautifulSoup(requests.get(url1).content, 'html5lib').get_text()
content2 = BeautifulSoup(requests.get(url2).content, 'html5lib').get_text()
#content1 = str(BeautifulSoup(open(url1).read(), features='html5lib'))
#content2 = str(BeautifulSoup(open(url2).read(), features='html5lib'))

def endcycle():
    print("endcycle() called", file=sys.stdout)
    with app.app_context():
        msg = Message('MSCWB',
        sender = 'ritts.1997@gmail.com',
        recipients = ['ritwikaghosh48@gmail.com', 'satanik.guha@gmail.com'])
        msg.body = 'Employee notice page or results page contents have changed. Check the site now!'
        mail.send(msg)
    print("Mail sent", file=sys.stdout)
    global content1
    global content2
    content1 = BeautifulSoup(requests.get(url1).content, 'html5lib').get_text()
    content2 = BeautifulSoup(requests.get(url2).content, 'html5lib').get_text()
    #content1 = str(BeautifulSoup(open(url1).read(), features='html5lib'))
    #content2 = str(BeautifulSoup(open(url2).read(), features='html5lib'))

def notifier():
    print("Notifier() called", file=sys.stdout)
    try:
        wbcontent1 = BeautifulSoup(requests.get(url1).content, 'html5lib').get_text()
        wbcontent2 = BeautifulSoup(requests.get(url2).content, 'html5lib').get_text()
        if wbcontent1 != content1 or wbcontent2 != content2:
            print("Page contents changed", file=sys.stdout)
            endcycle()
        else:
            print("Page contents same", file=sys.stdout)
    except Exception as e:
        print(e, file=sys.stderr)

scheduler.add_job(func=notifier, trigger="interval", minutes=10)
scheduler.start()

@app.route('/')
def index():
    c1 = BeautifulSoup(requests.get(url1).content, 'html5lib').title.get_text()
    c2 = BeautifulSoup(requests.get(url2).content, 'html5lib').title.get_text()
    res = "Employee notice title: " + c1 + "<br>Result title: " + c2
    return res
