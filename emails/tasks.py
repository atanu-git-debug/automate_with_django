from awd_main.celery import app
from dataentry.utils import send_email_notification

@app.task
def send_email_task(mail_sub,message,to_email,attachment):
    send_email_notification(mail_sub,message,to_email,attachment)
    return 'sending email task executed successfully!'