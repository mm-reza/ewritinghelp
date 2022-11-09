#pylint: disable = E1101
#pylint: disable = W0614

from django.core.mail import EmailMultiAlternatives, send_mail, EmailMessage, BadHeaderError
from django.core.exceptions import ValidationError

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from order.models import FOrderForm, FOrder
from user.models import*
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.template import loader
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.db.models import F
from home.models import Setting
import messagebird
import requests

######## File system  #########

@login_required(login_url='/login')
def addfile(request):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user
    if request.method == 'POST':  # if there is a post
        form = FOrderForm(request.POST, request.FILES)
        if form.is_valid():
            data = FOrder()
            data.first_name = form.cleaned_data['first_name']
            data.phone = form.cleaned_data['phone']
            data.files = form.cleaned_data['files']
            data.user_id = current_user.id
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(6).upper()  # random cod
            data.code = ordercode
            data.save()
            messages.success(request, 'Your file has ben sent. Please follow your dashboard for report')
            return redirect('/user')
        else:
            messages.warning(request, 'The maximum file size that can be uploaded is 2MB')      
            return HttpResponseRedirect(url)
    return render(request, 'F_Form.html')

