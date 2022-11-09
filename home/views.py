# pylint: disable=E1101  """#Class 'Setting' has no 'objects' memberpylint(no-member)#"""
# pylint: disable=W0614
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, request
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models.functions import Concat

from django.template.loader import render_to_string
from django.urls import reverse
import json
from ecom import settings


from user.models import UserProfile
from home.models import*
from home.forms import SearchForm

from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError

import requests
# Create your views here.

import re
  
def Find(string):
  
    # findall() has been used 
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)
    url_list = [x[0] for x in url]    
    return url_list


def home(request):
	settings = Setting.objects.get(pk=1)
	products = None
	
	categoryID = request.GET.get('category_id')

	current_user = request.user

	page = "home"

	
	# var = Product.objects.filter(title='dollar')
	context = {
			'settings': settings,
			'page': page,
			'products': products,
			}
	print(request.GET)
	return render(request, "home.html", context)


def aboutus(request):
	settings = Setting.objects.get(pk=1)
	context = {
		'settings': settings,
	}
	return render(request, "about.html", context)


def contactus(request):
	# Number can be added dynamicaly later
	#YOUR_ACCESS_KEY='8dd7f65dc9ddc818011ef7844f4b7c24'
	#url = 'http://apilayer.net/api/validate?access_key=8dd7f65dc9ddc818011ef7844f4b7c24&number=+8801723011523'

	# Making our request
	#response = requests.get(url)
	#data = response.json()

	# Your JSON object
	#print(data)
		
	if request.method == 'POST':  # check post
		form = ContactForm(request.POST)
		if form.is_valid():
			data = ContactMessage()  # create relation with model
			data.name = form.cleaned_data['name']  # get form input data
			data.email = form.cleaned_data['email']
			data.subject = form.cleaned_data['subject']
			data.message = form.cleaned_data['message']
			data.ip = request.META.get('REMOTE_ADDR')
			url = Find(data.message)
			if not url:
				data.save()  # save data to table
			messages.success(request, "Your message has ben sent. Thank you for your message.")
			return HttpResponseRedirect('/contact')

	setting = Setting.objects.get(pk=1)
	form = ContactForm
	context = {'setting': setting, 'form':form  }
	return render(request, 'contact.html', context)
	
	
	
def sitemap(request):
	return render(request, 'sitemap.xml')


def index(request):
	settings = Setting.objects.get(pk=1)
	context = {
		'settings': settings,
	}
	return render(request, "index.html", context)


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "accounts/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'ewritinghelps.com',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'noreply@ewritinghelps.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
			else: 
				messages.warning(request, 'invalid email')
				return render (request, "accounts/password_reset.html")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="accounts/password_reset.html", context={"password_reset_form":password_reset_form})


def bad_request(request, exception=None):
	return render(request, "errors/400.html", {}, status=400)

def permission_denied(request, exception=None):
	return render(request, "errors/403.html", {}, status=403)

def page_not_found(request, exception):
	return render(request, "errors/404.html", {}, status=404)

def server_error(request, exception=None):
	return render(request, "errors/500.html", {}, status=500)