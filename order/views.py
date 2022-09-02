#pylint: disable = E1101
#pylint: disable = W0614

from django.core.mail import EmailMultiAlternatives, send_mail, EmailMessage, BadHeaderError
from django.core.exceptions import ValidationError

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from order.models import ShopCart, ShopCartForm, OrderForm, Order, OrderProduct, FOrderForm, FOrder
from product.models import*
from product.models import Variants
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

# Create your views here.


def index(request):
    return HttpResponse("This is order page")


@login_required(login_url='/login')  # Check login
def addtoshopcart(request, id):
    ##url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    product = Product.objects.get(pk=id)

    if product.variant != 'None':
        variantid = request.POST.get('variantid')  # from variant add to cart
        checkinvariant = ShopCart.objects.filter(
            user_id=current_user.id)  # Check product in shopcart
        if checkinvariant:
            control = 1  # The product is in the cart
        else:
            control = 0  # The product is not in the cart"""
    else:
        checkinproduct = ShopCart.objects.filter(
            user_id=current_user.id)  # Check product in shopcart
        if checkinproduct:
            control = 1  # The product is in the cart
        else:
            control = 0  # The product is not in the cart"""

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:  # Update  shopcart
                messages.warning(request, "You already have it")
            else:  # Insert to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.variant_id = variantid
                data.quantity = form.cleaned_data['quantity']
                data.save()
                messages.success(request, "Product added to Shopcart ")
        return HttpResponseRedirect("/order/orderproduct")

    else:  # if there is no post
        if control == 1:  # Update  shopcart
            data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()  #
        else:  # Inser to Shopcart
            data = ShopCart()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.variant_id = None
            data.save()  #
        # messages.success(request, "Product added to Shopcart")
        return HttpResponseRedirect("/order/orderproduct")

@login_required(login_url='/login')  # Check login
def shopcart(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity

    subtotal = 0
    for rs in shopcart:
        subtotal += rs.quantity
    # return HttpResponse('ShopCart')
    context = {
        'shopcart': shopcart,
        'category': category,
        'total': total,
        'subtotal': subtotal,
    }
    return render(request, "shopcart_products.html", context)


@login_required(login_url='/login')  # Check login
def deletefromcart(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    ShopCart.objects.filter(id=id).delete()
    print(id)
    messages.success(request, "Your item deleted form Shopcart.")
    return HttpResponseRedirect(url)


""" @login_required(login_url='/login')  # Check login
def updatecart(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    qu= ShopCart.objects.filter(quantity=id)
    print(id)
    ShopCart.objects.filter(id=id).update(quantity=F('quantity')+10)
    print("quantity")
    messages.success(request, "Your item updated form Shopcart.")
    return HttpResponseRedirect(url) """


@login_required(login_url='/login')
def orderproduct(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = 0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.product.price * rs.quantity
        else:
            total += rs.variant.price * rs.quantity

    subtotal = 0
    for rs in shopcart:
        subtotal += rs.quantity

    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST, request.FILES)
        # return HttpResponse(request.POST.items())
        if form.is_valid():
            # Send Credit card to bank,  If the bank responds ok, continue, if not, show the error
            # ..............
            # Number can be added dynamicaly here
            phone=form.cleaned_data.get('phone')
            client = messagebird.Client('GOpk8EfQG0kRJ5E6cCJhowXN8')
            YOUR_ACCESS_KEY='8dd7f65dc9ddc818011ef7844f4b7c24'
            url = 'http://apilayer.net/api/validate?access_key=8dd7f65dc9ddc818011ef7844f4b7c24&number='+phone
            
            # Making our request
            response = requests.get(url)
            phones = response.json()
            carrier = phones["carrier"]
            number = phones["international_format"]
            home = phones["country_name"]
            # Your JSON object
            print(phones)
            print(carrier)
            if carrier and home !='':
                print(carrier)
            else:
                print("invalid number")
            
            print(home)
            data = Order()
            # get product quantity from form
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.files = form.cleaned_data['files']
            
            if carrier !='':
                data.phone_company = carrier.split()[0]
                data.phone_location = home.split()[0]
            else:
                data.phone_company = "invalid number"
                data.phone_location = home
                print("invalid number")

            data.country = form.cleaned_data['country']
            data.account = form.cleaned_data['account']
            data.user_id = current_user.id
            data.total = total
            data.subtotal = subtotal
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(6).upper()  # random cod
            data.code = ordercode
            data.save()

            total = 0
            for rs in shopcart:

                if rs.product.variant == 'None':
                    total += rs.product.price * rs.quantity
                else:
                    total += rs.variant.price * rs.quantity

                detail = OrderProduct()
                detail.order_id = data.id  # Order Id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                if rs.product.variant == 'None':
                    detail.price = rs.product.price
                else:
                    detail.price = rs.variant.price
                detail.variant_id = rs.variant_id
                if rs.product.variant == 'None':
                    detail.amount = rs.amount
                else:
                    detail.amount = rs.varamount
                detail.total = total
                detail.save()
                # ***Reduce quantity of sold product from Amount of Product
                if rs.product.variant == 'None':
                    product = Product.objects.get(id=rs.product_id)
                    product.amount -= rs.quantity
                    product.save()
                else:
                    variant = Variants.objects.get(id=rs.variant_id)
                    variant.quantity -= rs.quantity
                    variant.save()

            # ************ <> *****************

            # Clear & Delete shopcart
            ShopCart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_items'] = 0

            context = {
                'ordercode': ordercode,
                'category': category,
            }
            # ************ Sending Automated email *****************

            user = request.user
            profile = UserProfile.objects.get(user_id=request.user.id)
            context = {
                'shopcart': shopcart,
                'total': total,
                'profile': profile,
                'subtotal': subtotal,
                'user': user,
                'ordercode': ordercode,
            }




            #messagebird codes are below          
            try:              
                hlr = client.hlr_create('3067139740', 'MyReference')
                if carrier !='':
                    message = client.message_create(
                            'MessageBird',
                            '+8801723011523',
                            'Hi! This is your 252 message',
                            { 'reference' : 'Foobar' }
                        )
                    print('Message sent to', number)
                    print(message.__dict__)
                else:
                    print("Use a valid number")

                print(hlr.__dict__)

            except messagebird.client.ErrorException as e:
                for error in e.errors:
                    print(error)            
            
            """ #messagebird codes are below          
            try:              
                hlr = client.hlr_create('3067139740', 'MyReference')
                lookup_hlr = client.lookup_hlr_create('3067139740', { 'reference' : 'Reference' })
                lookup = client.lookup('+13067139740')
                if hlr.network is not None:
                    msg = client.message_create('sender_name', '+13068021664', 'test message')
                    print('error')
                    print(msg.__dict__)
                else:
                    print(hlr.network)


                print(hlr.__dict__)
                print(lookup.__dict__)
                print(lookup_hlr.__dict__)

            except messagebird.client.ErrorException as e:
                for error in e.errors:
                    print(error) """
            



            temp = render_to_string(
                'email.html', context)

            subject, from_email, to = 'Send with EmailMessage', 'bpanther70@gmail.com', 'bpanther70@gmail.com'
            text_content = 'This is an important message.'
            html_content = temp
            msg = EmailMessage(subject, temp, from_email, [to])
            msg.content_subtype = "html"  # Main content is now text/html

            msg.send()


            subject, from_email, to = 'EmailMultiAlternatives last', 'bpanther70@gmail.com', 'bpanther70@gmail.com'
            text_content = 'This is an important message.'
            html_content = temp
            msg = EmailMultiAlternatives(
            subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")

            if subject and temp and from_email:
                try:
                    msg.send()
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return HttpResponseRedirect('/order/complete/?ordercode=' + ordercode)
            else:
                 # In reality we'd use a form class
                 # to get proper validation errors.
                return HttpResponse('Make sure all fields are entered and valid.')     

            # ************ <> *****************

            messages.success(request, "Your Order has been completed. Thank you ")
            return HttpResponseRedirect('/order/complete/?ordercode=' + ordercode)
            # return HttpResponseRedirect("/order/complete", context)
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")

    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'shopcart': shopcart,
               'total': total,
               'form': form,
               'profile': profile,
               'subtotal': subtotal,
               
               }
    return render(request, 'Order_Form.html', context)


@login_required(login_url='/login')  # Check login
def complete(request):
    profile = UserProfile.objects.get(user_id=request.user.id)
    ordercode= request.GET.get('ordercode')
    
    context = {
        'ordercode':ordercode,
        'profile': profile,     
    }
    return render(request, "Order_Completed.html", context)


def convert(request):
    return render(request, 'convert.html')

def send_update(sender, instance, created, **kwargs):   
    admin= Setting.email
    if instance.status=='Accepted':
        order=instance.id
        products = OrderProduct.objects.filter(order_id=instance.id)
        context={
            'instance':instance,
            'products':products,
        }           
        temp = render_to_string('update.html', context)
        subject, from_email = 'Send with EmailMessage', 'admin'
        text_content = 'Oder Accepted  {{instance.address}} , instance.address  "instance.total" {{"instance.total"}} ["instance.total"]'
        html_content = temp
        msg = EmailMessage(subject, temp, from_email, [instance.address,])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()
        print(instance.total)
        print(instance.id)
        print('order.id')
    elif instance.status=='Canceled':
        temp = render_to_string('update.html')
        subject, from_email = 'Send with EmailMessage', 'admin'
        text_content = 'Order cancled.'
        html_content = temp
        msg = EmailMessage(subject, text_content, from_email, [instance.address,])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()
post_save.connect(send_update, sender=Order)


@login_required(login_url='/login')  # Check login
def updatecart(request, id):
    #url = request.META.get('HTTP_REFERER')  # get last url
    #current_user = request.user  # Access User Session information
    #data = ShopCart.objects.get(id=id, user_id=current_user.id)
    #data.quantity = +1
    #data.save()  #

    # messages.success(request, "Product added to Shopcart")
    # return HttpResponseRedirect("/order/orderproduct")

    url = request.META.get('HTTP_REFERER')  # get last url
    if request.method == 'POST':  # if there is a post
        
        form = ShopCartForm(request.POST)
        if form.is_valid():
                    
            data = ShopCart.objects.get(id=id)
            mini = Variants.objects.get(id=data.variant_id)  
            data.quantity = form.cleaned_data['quantity']
            data.save()  # save data
            messages.success(request, "Product added to Shopcart ")
            
            context={
                'mini':mini,
            }
            print(mini.quantity)
            return HttpResponseRedirect(url, context)
        else:
            messages.warning(request,"Value is not valid")
            return HttpResponseRedirect(url)




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

