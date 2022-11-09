# pylint: disable=W0614
# pylint: disable=E1101
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from order.models import*
from user.models import*
from user.models import UserProfile
from.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, BadHeaderError
from.tokens import account_activation_token

# Create your views here.


@login_required(login_url='/login')  # Check login
def index(request):

	current_user = request.user
	profile = UserProfile.objects.get(user_id=current_user.id)
	recent_files = FOrder.objects.filter(user_id=current_user.id).order_by('-id')[:1]
	context = {
			'profile': profile,
			'recent_files':recent_files,
		}
	return render(request, 'user_dash.html', context)


def login_form(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			current_user = request.user
			userprofile = UserProfile.objects.get(user_id=current_user.id)
			request.session['userimage'] = userprofile.image.url
			# Redirect to a success page.
			return HttpResponseRedirect('/')
		else:
			messages.warning(
				request, "Login Error !! Username or Password is incorrect")
			return HttpResponseRedirect('/login')
	else:
		return render(request, "login.html")


def logout_func(request):
	logout(request)
	return HttpResponseRedirect('/')


def signup_form(request):
	
	url = request.META.get('HTTP_REFERER')  # get last url
	if request.method == 'POST':
		form = SignUpForm(request.POST)

		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			current_site = get_current_site(request)
			email_subject = 'Activate Your Account'
			message = render_to_string('activate_account.html', {
			'user': user,
			'domain': current_site.domain,
			'uid': urlsafe_base64_encode(force_bytes(user.pk)),
			'token': account_activation_token.make_token(user),
			})
			to_email = form.cleaned_data.get('email')
			email = EmailMessage(email_subject, message, 'noreply@ewritinghacks.com', to=[to_email])
			email.send()
			return HttpResponse('We have sent you an email, please confirm your email address to complete registration')
		else:
			print(form.errors)
			print(form.fields)
			error= form.errors
			messages.warning(request, error)		
			form = SignUpForm()
			context = {
					'form': form,
					'error': error,
					}
			return render(request, 'signup.html', context)
			
	form = SignUpForm()
	context = {
			   'form': form,
			   }
	return render(request, 'signup.html', context)


@login_required(login_url='/login')  # Check login
def user_update(request):
	url = request.META.get('HTTP_REFERER')  # get last url
	if request.method == 'POST':
		# request.user is user  data
		user_form = UserUpdateForm(request.POST, instance=request.user)
		profile_form = ProfileUpdateForm(
			request.POST, request.FILES, instance=request.user.userprofile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()			
			messages.success(request, 'Your account has been updated!')
			return HttpResponseRedirect('/user')
		else:
			messages.warning(request, 'Your account has not been updated, please try again!')		
			return redirect(url)
	else:

		user_form = UserUpdateForm(instance=request.user)
		# "userprofile" model -> OneToOneField relatinon with user
		profile_form = ProfileUpdateForm(instance=request.user.userprofile)
		context = {
			'user_form': user_form,
			'profile_form': profile_form,
		}
		return render(request, 'user_update.html', context)


@login_required(login_url='/login')  # Check login
def password_update(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, 'Your password was successfully updated!')
			return HttpResponseRedirect("/user")
		else:
			messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
			return HttpResponseRedirect("/user/password")
	else:
		# category = Category.objects.all()
		form = PasswordChangeForm(request.user)
		return render(request, 'user_password.html', {'form': form,  # 'category': category
 })

@login_required(login_url='/login') # Check login
def reply(request,id):
   url = request.META.get('HTTP_REFERER')  # get last url
   #return HttpResponse(url)
   if request.method == 'POST':  # check post
      form = ReplyForm(request.POST, request.FILES)
      if form.is_valid():
         data = Reply()  # create relation with model
         data.subject = form.cleaned_data['subject']
         data.reply = form.cleaned_data['reply']
         data.image = form.cleaned_data['image']
         data.ip = request.META.get('REMOTE_ADDR')
         data.order_id=id
         current_user= request.user
         data.user_id=current_user.id
         data.save()  # save data to table
         messages.success(request, "Your review has ben sent. Thank you for your interest.")
         return HttpResponseRedirect(url)
      else:
         messages.warning(request, 'The maximum file size that can be uploaded is 2MB / Max size of file is 2 MB')      
         return HttpResponseRedirect(url)
   return HttpResponseRedirect(url)

@login_required(login_url='/login') # Check login
def user_replys(request):
	current_user = request.user
	replys = Reply.objects.filter(user_id=current_user.id).order_by('-id')
	context = {
		'replys': replys,
	}
	return render(request, 'user_replys.html', context)



def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        #Create data in profile table for user
        current_user = request.user
        data = UserProfile()
        data.email_confirmed = True
        data.user_id = current_user.id
        data.email = current_user.email
        data.image = "images/placeholder.png"
        data.save()
        messages.success(request, 'Your account has been activate successfully')
        return HttpResponseRedirect('/')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required(login_url='/login') # Check login
def files(request):
	current_user = request.user
	ufiles = FOrder.objects.filter(user_id=current_user.id).order_by('-id')
	context = {
		'ufiles': ufiles,
	}
	return render(request, 'user_files.html', context)

@login_required(login_url='/login') # Check login
def user_deletefiles(request,id):
	current_user = request.user
	FOrder.objects.filter(id=id, user_id=current_user.id).delete()
	messages.success(request, 'File deleted..')
	return HttpResponseRedirect('/user/files')