from django.shortcuts import render,redirect
from .forms import EmailForm
from django.contrib import messages
from dataentry.utils import send_email_notification
from django.conf import settings
from .models import Subscriber
# Create your views here.
def send_emails(request):
    if request.method == 'POST':
        email_form = EmailForm(request.POST,request.FILES)
        if email_form.is_valid():
            email_form = email_form.save()
            #send email
            mail_sub = request.POST.get('subject')
            message = request.POST.get('body')
            email_list = request.POST.get('email_list')
            
            # Access the selected list

            email_list = email_form.email_list
            # Extract email addresses from the email model
            
            subscriber = Subscriber.objects.filter(email_list=email_list)
            to_email = [email.email_address for email in subscriber]

            if email_form.attacthment:
                attachment = email_form.attacthment.path
            else:
                attachment = None
            send_email_notification(mail_sub,message,to_email,attachment)
           
            #display a success message
            messages.success(request,"Email sent successfuly!")

            return redirect('send_emails')
    else:
        email_form = EmailForm()
        context = {
            'email_form' : email_form
        }
    return render(request,'emails/send-emails.html',context)