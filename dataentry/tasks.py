from awd_main.celery import app
import time
from django.core.management import call_command
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import send_email_notification,generate_csv_file

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
        to_mail = []
        to_mail.append(settings.DEFAUL_TO_EMAIL) 
        send_email_notification(mail_sub,message,to_mail)
        return 'Data imported successfully'

@app.task
def export_data_task(model_name):
    try:
            call_command("exportdata",model_name)
    except Exception as e:
        raise e
    file_path = generate_csv_file(model_name)
    
    # send email with attachment
    mail_sub = "Export Data successful"
    message = "Export Data successful please finde the attachment"
    to_mail = []
    to_mail.append(settings.DEFAUL_TO_EMAIL)
    send_email_notification(mail_sub,message,to_mail,attachment=file_path)
    return "Export data task executed sucessfully"