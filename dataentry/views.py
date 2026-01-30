from django.shortcuts import render,redirect
from .utils import get_all_custom_models
from uploads.models import Upload
from django.conf import settings
from django.core.management import call_command
from django.http import HttpResponse as httpResponse
from django.contrib import messages
# Create your views here.
def import_data(request):
    if request.method == 'POST':
        # Handle file upload and data import logic here

        file_path = request.FILES.get('file_path')
        model_name = request.POST.get('model_name')

        # store the file inside Upload model

        upload = Upload.objects.create(file=file_path, model_name=model_name)
        
        #construct the full path
        relative_path = upload.file.url
        base_url = settings.BASE_DIR
        file_path = str(base_url) + str(relative_path)

        # trigger the data import data command
        try:
            call_command('importdata',file_path,model_name)
            messages.success(request, f"Data imported successfully into {model_name} table.")
        except Exception as e:
            messages.error(request, f"Error importing data into {model_name} table: {e}")

        return redirect('import_data')
    else:
        all_models = get_all_custom_models()
        context = {
            'all_models': all_models
        }    
    return render(request,'dataentry/import_data.html',context)