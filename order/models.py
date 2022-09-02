#pylint: disable = E1101
#pylint: disable = W0614

from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from product.models import*
from django.core.validators import MinValueValidator, MaxValueValidator
from home.validators import validate_file_size
from django.http import HttpResponse

# Create your models here.

class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL,blank=True, null=True) # relation with varinat
    quantity = models.IntegerField(validators=[MinValueValidator(3),
                                       MaxValueValidator(50000)])
    def __str__(self):
        return self.product.title

    @property
    def price(self):
        return (self.product.price)

    @property
    def amount(self):
        return (self.quantity * self.product.price)
    
    @property
    def varamount(self):
        return (self.quantity * self.variant.price)

    # method to create a fake table field in read only mode

    def img_tag(self):
        if self.image is not None:
            return mark_safe('<img src="/uploads/%s" height="25" width="35"/>' % (self.image))
        else:
            return 'images/placeholder.png'

    # def image_tag(self):
    # return mark_safe('<img src="/uploads/%s" width="50" />' % (self.image))

    img_tag.short_description = 'Img'

class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Preaparing', 'Preaparing'),
        ('OnShipping', 'OnShipping'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=6, editable=False)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=10, blank=True)
    phone = models.CharField(blank=True, max_length=15)
    phone_company = models.CharField(blank=True, max_length=20)
    phone_location = models.CharField(blank=True, max_length=20)

    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=30)
    country = models.CharField(blank=True, max_length=20)
    account = models.CharField(blank=True, max_length=30)
    total = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    adminnote = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    files = models.FileField(upload_to='images/', blank=True, default='images/placeholder.png', validators=[validate_file_size])


    def __str__(self):
        return str(self.id)


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name',
                  'address', 'phone', 'city', 'country', 'account', 'files']


class OrderProduct(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL,blank=True, null=True) # relation with varinat
    quantity = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title


########## File system #########


class FOrder(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Preaparing', 'Preaparing'),
        ('OnShipping', 'OnShipping'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=6, editable=False)
    first_name = models.CharField(max_length=30, blank=False)
    phone = models.EmailField(max_length=25, blank=False)
    status = models.CharField(max_length=20, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    adminnote = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    files = models.FileField(upload_to='images/', blank=False, validators=[validate_file_size])
    reports = models.FileField(upload_to='images/', blank=True, validators=[validate_file_size])

    def __str__(self):
        return str(self.id)
    
    @property
    def reports_url(self):
        if self.reports and hasattr(self.reports, 'url'):
            return self.reports.url
        else:
            return "Not Ready"

class FOrderForm(ModelForm):
    class Meta:
        model = FOrder
        fields = ['first_name', 'phone', 'files']
