from awd_main.celery import app
from dataentry.utils import send_email_notification

@app.task
def send_email_task(mail_sub,message,to_email,attachment,email_id):
    send_email_notification(mail_sub,message,to_email,attachment,email_id)
    return 'sending email task executed successfully!'