from awd_main.celery import app
import time
from django.core.management import call_command
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import send_email_notification

@app.task
def celery_test_task():
        time.sleep(5)
        #send email
        mail_sub = "This is a test email"
        message = "Email sent successful"
        to_mail = settings.DEFAUL_TO_EMAIL
        send_email_notification(mail_sub,message,to_mail)
        return 'Email send successfully'

@app.task
def import_data_task(file_path,model_name):
        try:
            call_command('importdata',file_path,model_name)
            
        except Exception as e:
            raise e
        # send the user email to notify
        mail_sub = "Import data completed"
        message = "Your data import has been successful"
        to_mail = settings.DEFAUL_TO_EMAIL
        send_email_notification(mail_sub,message,to_mail)
        return 'Data imported successfully'