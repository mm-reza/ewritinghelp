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
from product.models import*
from order.views import shopcart, ShopCart
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
	category = Category.objects.all()
	products = None
	
	categories = Category.get_all_categories()
	categoryID = request.GET.get('category_id')

	current_user = request.user
	shopcart = ShopCart.objects.filter(user_id=current_user.id)

	subtotal = 0

	for rs in shopcart:
		subtotal += rs.quantity
	
	if categoryID:
		products = Product.get_all_products_by_categoryid(categoryID)
	else:
		products = Product.get_all_products()

	page = "home"
	product_home = Product.objects.all()
	product_slider = Product.objects.all().order_by('-id')[:3]
	product_latest = Product.objects.all().order_by('-id')[:4]
	product_random = Product.objects.all().order_by('?')[:4]
	
	var = Product.objects.filter(title='dollar')
	context = {
			'var': var,
			'product_home': product_home,
			'product_slider': product_slider,
			'product_latest': product_latest,
			'product_random': product_random,
			'settings': settings,
			'category': category,
			'page': page,
			'products': products,
			'categories':categories,
			'subtotal': subtotal,
			}
	print(request.GET)
	print(categories)
	return render(request, "home.html", context)


def aboutus(request):
	category = Category.objects.get(pk=id)
	settings = Setting.objects.get(pk=1)
	context = {
		'category': category,
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
			messages.success(
				request, "Your message has ben sent. Thank you for your message.")
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


def category_products(request, id, slug):

	category = Category.objects.get(pk=id)
	products = Product.objects.filter(category_id=id)  # default language
	context = {'products': products,
			   'category': category,
			   # 'catdata':catdata,
			   }
	return render(request, 'category_products.html', context)

def search(request):
	if request.method == 'POST': # check post
		form = SearchForm(request.POST)
		if form.is_valid():
			query = form.cleaned_data['query'] # get form input data
			catid = form.cleaned_data['catid']
			if catid==0:
				products=Product.objects.filter(title__icontains=query)  #SELECT * FROM product WHERE title LIKE '%query%'
			else:
				products = Product.objects.filter(title__icontains=query,category_id=catid)

			category = Category.objects.all()
			context = {'products': products, 'query':query,
					   'category': category }
			return render(request, 'search_products.html', context)

	return HttpResponseRedirect('/')


def side(request):
	settings = Setting.objects.get(pk=1)
	product_slider = Product.objects.all().order_by('-id')[:3]
	context = {
		'settings': settings,
		'product_slider': product_slider,
	}
	return render(request, "side.html", context)

def product_detail(request,id,slug):
	query = request.GET.get('q')
	category = Category.objects.all
	product = Product.objects.get(pk=id)  # default language
	images = Images.objects.filter(product_id=id)
	comments = Comment.objects.filter(product_id=id,status='True')
	shopcart = ShopCart.objects.all()
	subtotal = 0
	for rs in shopcart:
		subtotal += rs.quantity
	context = {'product': product,
			   'category': category,
			   'images': images,
			   'comments': comments,
			   'subtotal':subtotal,
			   }
	if product.variant !="None": # Product have variants
		if request.method == 'POST': #if we select colorz
			variant_id = request.POST.get('variantid')
			variant = Variants.objects.get(id=variant_id) #selected product by click color radio
			colors = Variants.objects.filter(product_id=id,size_id=variant.size_id )
			sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
			query = variant.title+' Size:' +str(variant.size) +' Color:' +str(variant.color)
		else:
			variants = Variants.objects.filter(product_id=id)
			colors = Variants.objects.filter(product_id=id,size_id=variants[0].size_id )
			sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
			variant =Variants.objects.get(id=variants[0].id)
		context.update({'sizes': sizes, 'colors': colors,
						'variant': variant,'query': query
						})
	return render(request,'product_detail.html',context)


def product_dollar(request,id,slug):
	query = request.GET.get('q')
	category = Category.objects.all
	product = Product.objects.get(pk=id)  # default language
	images = Images.objects.filter(product_id=id)
	comments = Comment.objects.filter(product_id=id,status='True')

	current_user = request.user
	shopcart = ShopCart.objects.filter(user_id=current_user.id)
	subtotal = 0
	for rs in shopcart:
		subtotal += rs.quantity

	context = {'product': product,
			   'category': category,
			   'images': images,
			   'comments': comments,
			   'subtotal':subtotal,
			   }
	if product.variant !="None": # Product have variants
		if request.method == 'POST': #if we select color
			variant_id = request.POST.get('variantid')
			variant = Variants.objects.get(id=variant_id) #selected product by click color radio
			colors = Variants.objects.filter(product_id=id,size_id=variant.size_id )
			sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
			query = variant.title+' Size:' +str(variant.size) +' Color:' +str(variant.color)
		else:
			variants = Variants.objects.filter(product_id=id)
			colors = Variants.objects.filter(product_id=id,size_id=variants[0].size_id )
			sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
			variant =Variants.objects.get(id=variants[0].id)
		context.update({'sizes': sizes, 'colors': colors,
						'variant': variant,'query': query
						})
	return render(request,'dollar.html',context)


def estimate(request):
	product = Product.objects.get(id='14')  # default language
	images = Images.objects.filter(product_id='14')
	comments = Comment.objects.filter(product_id='14',status='True')

	current_user = request.user
	shopcart = ShopCart.objects.filter(user_id=current_user.id)
	subtotal = 0
	for rs in shopcart:
		subtotal += rs.quantity

	context = {'product': product,
			   'images': images,
			   'comments': comments,
			   'subtotal':subtotal,
			   }
	if product.variant !="None": # Product have variants
		if request.method == 'POST': #if we select color
			variant_id = request.POST.get('variantid')
			variant = Variants.objects.get(id=variant_id) #selected product by click color radio
			colors = Variants.objects.filter(product_id='14',size_id=variant.size_id )
			sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',['14'])
			
		else:
			variants = Variants.objects.filter(product_id='14')
			colors = Variants.objects.filter(product_id='14',size_id=variants[0].size_id )
			sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',['14'])
			variant =Variants.objects.get(id=variants[0].id)
		context.update({'sizes': sizes, 
						'colors': colors,
						'variant': variant,
						})
	return render(request,'dollar.html',context)

def ajaxcolor(request):
	data = {}
	if request.POST.get('action') == 'post':
		size_id = request.POST.get('size')
		productid = request.POST.get('productid')
		colors = Variants.objects.filter(product_id=productid, size_id=size_id)
		context = {
			'size_id': size_id,
			'productid': productid,
			'colors': colors,
		}
		data = {'rendered_table': render_to_string('color_list.html', context=context)}
		return JsonResponse(data)
	return JsonResponse(data)



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
					'domain':'ewritinghacks.com',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'noreply@ewritinghacks.com' , [user.email], fail_silently=False)
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