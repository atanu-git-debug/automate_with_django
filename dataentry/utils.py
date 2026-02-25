import hashlib
import time
from django.apps import apps
from django.core.management.base import CommandError
import csv
import os
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings
import datetime
from emails.models import Email,Sent,EmailTracking, Subscriber
from bs4 import BeautifulSoup

def get_all_custom_models():
    default_models = {'LogEntry', 'ContentType', 'Session', 'Group', 'Permission','Upload'}
    custom_models = []
    for model in apps.get_models():
        if model.__name__ not in default_models:
            custom_models.append(model.__name__)
    return custom_models

def check_csv_errors(file_path,model_name):
    model = None
    # search for the model across all the installed apps
    for app_config in apps.get_app_configs():
            #try to search for the model in the app
        try:
            model = apps.get_model(app_config.label,model_name)
            break
        except LookupError:
            continue


    if not model:
        raise CommandError(f"Model {model_name} not found in any installed app.")
    # get the field names of the model that we found
    model_fields = [field.name for field in model._meta.fields if field.name != 'id']
    try:
        with open(file_path,'r')as f:
            reader = csv.DictReader(f)
            csv_header = reader.fieldnames

                #comapre cse header and model's field
            if csv_header != model_fields:
                raise DataError(f"CSV doesn't match with the {model_name} fields")
    except Exception as e:
        raise e
    return model


def send_email_notification(mail_sub,message,to_email,attachment=None,email_id=None):

    try:
        from_email  = settings.DEFAUL_FROM_EMAIL
        for recipent_email in to_email:
            new_message = message
            # create email trackin recorde
            if email_id:
                email = Email.objects.get(pk=email_id)
                subscriber = Subscriber.objects.get(email_list=email.email_list,email_address=recipent_email)
                timestamp = str(time.time())
                data_to_hash = f"{recipent_email}{timestamp}"
                unique_id = hashlib.sha256(data_to_hash.encode()).hexdigest()
                email_tracking = EmailTracking.objects.create(
                    email = email,
                    subscriber = subscriber,
                    unique_id = unique_id
                )                   
                #generate the tracking pixel
                base_url = settings.BASE_URL
                click_tracking_url = f"{base_url}/emails/track/click/{unique_id}"
                open_tracking_url = f"{base_url}/emails/track/open/{unique_id}"
                

                # search for the links in email body
                soup = BeautifulSoup(message,'html.parser')
                urls = [url['href'] for url in soup.find_all('a',href=True)]
                
                # If there are links or url in the eamil body , inject our trackin url to that
                if urls :
                    for url in urls:
                        
                        # make the final tracking url
                        tracking_url = f"{click_tracking_url}?url={url}"
                        print(f'tracking_url: {tracking_url}')
                        new_message = new_message.replace(f'{url}',f'{tracking_url}')
                else:
                    
                    print('No urls Found in the email content')
                
                # Create the em email content with the open tracking pixel
                open_tracking_img = f"<img src='{open_tracking_url}' width='1' height='1'>"
                new_message += open_tracking_img
            

            mail = EmailMessage(mail_sub,new_message,from_email,to=[recipent_email])
            if attachment is not None:
                mail.attach_file(attachment)
        
        mail.content_subtype = 'html'
        mail.send()
        # store the total sent emails
        if email_id:
            sent = Sent()
            sent.email = email
            sent.total_sent = email.email_list.count_emails()
            sent.save()
    except Exception as e:
        raise e
    
def generate_csv_file(model_name):
        # get current timestamp for unique file naming
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        # define the CSV file path and file name
        export_dir = 'exported_data'
        file_name = f"exported_{model_name}_data_{timestamp}.csv"
        file_path = os.path.join(settings.MEDIA_ROOT,export_dir,file_name)
        
        return file_path