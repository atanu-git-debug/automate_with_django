import csv
from django.core.management.base import BaseCommand
from django.apps import apps
import datetime

# proposed command = manage.py exportdata "model_name"



class Command(BaseCommand):

    



    help = "Exports data from the database to a CSV file"

    def add_arguments(self,parser):
        parser.add_argument('model_name',type=str,help="Name of the model to export data from")

    def handle(self, *args, **kwargs):

        model_name = kwargs['model_name'].capitalize()
        model = None

        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label,model_name)
                break
            except LookupError:
                continue
        if not model:
            self.stdout.write(self.style.ERROR(f"Model {model_name} not found in any installed app."))
            return
        #fetch data from the database
        data = model.objects.all()
        

        # get current timestamp for unique file naming
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        # define the CSV file path and file name
        file_path = f"exported_{model_name}_data_{timestamp}.csv"
        
        # open the CSV file in write mode and write data to it
        with open(file_path,mode='w',newline='') as f:

            writer = csv.writer(f)
            # write the header row
            # fields names of the model
            writer.writerow([field.name for field in model._meta.fields])
            # write data rows
            for dat in data:
                writer.writerow([getattr(dat,field.name) for field in model._meta.fields])
        

        self.stdout.write(self.style.SUCCESS("data exported successfully"))