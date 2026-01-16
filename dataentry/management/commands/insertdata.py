from django.core.management.base import BaseCommand
from dataentry.models import Student
#want to insert data into the database using a custom management command

class Command(BaseCommand):

    help = "Inserts data into the database"

    def handle(self, *args, **kwargs):

        # logic 

        dataset =[
            {'name':'Sanchari', 'roll_no':'100', 'age':22},
            {'name':'Raju', 'roll_no':'102', 'age':23},
            {'name':'Mita', 'roll_no':'103', 'age':21},
            {'name':'Anik', 'roll_no':'104', 'age':24},
            {'name':'Rina', 'roll_no':'105', 'age':22},
            {'name':'Sneha', 'roll_no':'106', 'age':23},

        ]
        for data in dataset:
            roll_no = data['roll_no']
            exisiting_record = Student.objects.filter(roll_no=roll_no).exists()

            if not exisiting_record:
                Student.objects.create(name=data['name'], roll_no=data['roll_no'], age=data['age'])
            else:
                self.stdout.write(self.style.WARNING(f"Record with roll_no {roll_no} already exists. Skipping insertion."))
        
        
        self.stdout.write(self.style.SUCCESS("Data inserted successfully"))
