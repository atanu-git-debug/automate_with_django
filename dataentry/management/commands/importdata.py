from django.core.management.base import BaseCommand, CommandError
import csv
from django.apps import apps
from django.db import DataError
from dataentry.utils import check_csv_errors

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
        
        model = check_csv_errors(file_path,model_name)
        #compare csv header with model's fiels names 
        
        with open(file_path,'r') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                model.objects.create(**row)        
        
        self.stdout.write(self.style.SUCCESS("Data imported from CSV Successfully"))