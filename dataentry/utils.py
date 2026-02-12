from django.apps import apps
from django.core.management.base import CommandError
import csv
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings


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


def send_email_notification(mail_sub,message,to_email):

    try:
        from_email  = settings.DEFAUL_FROM_EMAIL


        mail = EmailMessage(mail_sub,message,from_email,to=[to_email])
        mail.send()
    except Exception as e:
        raise e
