from django.core.management.base import BaseCommand

#proposed command = python manage.py greeting 
#proposed output = Hello {<user_name>} , Whats up

class Command(BaseCommand):

    help = "Greets the user"

    def add_arguments(self, parser):
        
        parser.add_argument('name',type=str,help="specifies user name")

    def handle(self,*args,**kwargs):

        name = kwargs['name']
        greeting = f"Hello {name}, Whats up"
        self.stdout.write(self.style.SUCCESS(greeting))