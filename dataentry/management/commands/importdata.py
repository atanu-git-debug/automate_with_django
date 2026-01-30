from django.core.management.base import BaseCommand, CommandError
import csv
from django.apps import apps
from django.db import DataError

#proposed command = manage.py importdata file_path model_name

class Command(BaseCommand):

    help = "import data into the application"

    def add_arguments(self, parser):
        parser.add_argument('file_path',type=str,help="Path to the csv file")
        parser.add_argument('model_name',type=str,help="Name of the model to import data into")

    def handle(self,*args,**kwargs):

        #logic
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()
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

        #compare csv header with model's fiels names 
        # get the field names of the model that we found
        model_fields = [field.name for field in model._meta.fields if field.name != 'id']
        


        with open(file_path,'r')as f:
            reader = csv.DictReader(f)
            csv_header = reader.fieldnames

            #comapre cse header and model's field
            if csv_header != model_fields:
                raise DataError(f"CSV doesn't match with the {model_name} fields")

            for row in reader:
                model.objects.create(**row)        
        
        self.stdout.write(self.style.SUCCESS("Data imported from CSV Successfully"))