from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from .forms import EmailForm
from django.contrib import messages
from dataentry.utils import send_email_notification
from django.conf import settings
from .models import Subscriber,Email,Sent,EmailTracking
from django.contrib.auth.decorators import login_required
from .tasks import send_email_task
from django.db.models import Sum
from django.utils import timezone
# Create your views here.
@login_required(login_url='login')
def send_emails(request):
    if request.method == 'POST':
        email = EmailForm(request.POST,request.FILES)
        if email.is_valid():
            email = email.save()
            #send email
            mail_sub = request.POST.get('subject')
            message = request.POST.get('body')
            email_list = request.POST.get('email_list')
            
            # Access the selected list

            email_list = email.email_list
            # Extract email addresses from the email model
            
            subscriber = Subscriber.objects.filter(email_list=email_list)
            to_email = [email.email_address for email in subscriber]

            if email.attacthment:
                attachment = email.attacthment.path
            else:
                attachment = None

            email_id = email.id
            # Handover email sendin task to celery
            send_email_task.delay(mail_sub,message,to_email,attachment,email_id)
            
           
            #display a success message
            messages.success(request,"Email sent successfuly!")

            return redirect('send_emails')
    else:
        email = EmailForm()
        context = {
            'email_form' : email
        }
    return render(request,'emails/send-emails.html',context)
@login_required(login_url='login')
def track_dashboard(request):
    emails = Email.objects.all().annotate(total_sent=Sum('sent__total_sent')).order_by('-sent_at')

    
    context = {
        'emails' : emails
    }
    return render(request,'emails/track_dashboard.html',context)
@login_required(login_url='login')
def track_click(request,unique_id):
    try:
        email_tracking = EmailTracking.objects.get(unique_id=unique_id)
        url = request.GET.get('url')
        # check if the clicked at filed is already set or not
        if not email_tracking.clicked_at:
            email_tracking.clicked_at = timezone.now()
            email_tracking.save()
            return HttpResponseRedirect(url)
        else:
            return HttpResponseRedirect(url)
    except:
        return HttpResponse('Email tracking recorde not fornd')
@login_required(login_url='login')
def track_open(request,unique_id):
    try:
        email_tracking = EmailTracking.objects.get(unique_id=unique_id)
        # check if the opend at filed is already set or not
        if not email_tracking.opened_at:
            email_tracking.opened_at= timezone.now()
            email_tracking.save()
            return HttpResponse('Email opend successfuly!')
        else:
            return HttpResponse('Email opend already')
    except:
        return HttpResponse('Email tracking recorde not fornd') 
@login_required(login_url='login')
def track_stats(request,pk):
    email = get_object_or_404(Email,pk=pk)
    sent = Sent.objects.get(email=email)
    context = {
        'email' : email,
        'total_sent' : sent.total_sent
    }
    return render(request,'emails/track_stats.html',context)