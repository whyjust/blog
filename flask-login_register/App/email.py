from flask import render_template,current_app
from flask_mail import Message
from threading import Thread
from App.extensions import mail


def async_send_mail(app,msg):
    with app.app_context():
        mail.send(message=msg)


def send_mail(subject,to,tem,**kwargs):
    app = current_app._get_current_object()
    msg = Message(subject=subject, recipients=[to], sender=app.config['MAIL_USERNAME'])
    msg.html = render_template('email/'+tem+'.html',**kwargs)
    send = Thread(target=async_send_mail,args=(app,msg))
    send.start()