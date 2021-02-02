import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_mail import Mail, Message
from bs4 import BeautifulSoup
import requests
import html5lib
import sys

app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ritts.1997@gmail.com'
app.config['MAIL_PASSWORD'] = '1234Abcd'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_SUPRESS_SEND'] = False
app.config['DEBUG'] = True
app.config['TESTING'] = False
mail = Mail(app)
msg = Message('MSCWB',
    sender = 'ritts.1997@gmail.com',
    recipients = ['ritwikaghosh48@gmail.com', 'satanik.guha@gmail.com'])
msg.body = 'Page contents have changed. Check the site now!'
url = 'https://www.mscwb.org/home/emp_notice'
print(url, file=sys.stdout)

scheduler = BackgroundScheduler()

title = BeautifulSoup(requests.get(url).content, 'html5lib').get_text()

def endcycle():
    print("endcycle() called", file=sys.stdout)
    with app.app_context():
        mail.send(msg)
    print("Mail sent", file=sys.stdout)
    global title
    title = BeautifulSoup(requests.get(url).content, 'html5lib').get_text()

def notifier():
    print("Notifier() called", file=sys.stdout)
    try:
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'html5lib')
        wbtitle = soup.get_text()
        if wbtitle != title:
            print("Page contents changed", file=sys.stdout)
            endcycle()
        else:
            print("Page contents same", file=sys.stdout)
    except Exception as e:
        print(e, file=sys.stderr)

scheduler.add_job(func=notifier, trigger="interval", minutes=2)
scheduler.start()

@app.route('/')
def index():
    return BeautifulSoup(requests.get(url).content, 'html5lib').title.get_text()
    
