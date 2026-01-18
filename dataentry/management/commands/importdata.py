from django.core.management.base import BaseCommand, CommandError
import csv
from django.apps import apps

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



        with open(file_path,'r')as f:
            reader = csv.DictReader(f)
            for row in reader:
                model.objects.create(**row)        
        
        self.stdout.write(self.style.SUCCESS("Data imported from CSV Successfully"))