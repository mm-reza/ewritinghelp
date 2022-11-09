#pylint: disable = E1101
#pylint: disable = W0614

from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.validators import MinValueValidator, MaxValueValidator
from home.validators import validate_file_size
from django.http import HttpResponse

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



######## End Filesystem #########




# class Order(models.Model):
#     STATUS = (
#         ('New', 'New'),
#         ('Accepted', 'Accepted'),
#         ('Preaparing', 'Preaparing'),
#         ('OnShipping', 'OnShipping'),
#         ('Completed', 'Completed'),
#         ('Canceled', 'Canceled'),
#     )
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     code = models.CharField(max_length=6, editable=False)
#     first_name = models.CharField(max_length=30, blank=True)
#     last_name = models.CharField(max_length=10, blank=True)
#     phone = models.CharField(blank=True, max_length=15)
#     phone_company = models.CharField(blank=True, max_length=20)
#     phone_location = models.CharField(blank=True, max_length=20)

#     address = models.CharField(blank=True, max_length=150)
#     city = models.CharField(blank=True, max_length=30)
#     country = models.CharField(blank=True, max_length=20)
#     account = models.CharField(blank=True, max_length=30)
#     total = models.FloatField()
#     status = models.CharField(max_length=20, choices=STATUS, default='New')
#     ip = models.CharField(blank=True, max_length=20)
#     adminnote = models.CharField(blank=True, max_length=100)
#     create_at = models.DateTimeField(auto_now_add=True)
#     update_at = models.DateTimeField(auto_now=True)
#     files = models.FileField(upload_to='images/', blank=True, default='images/placeholder.png', validators=[validate_file_size])


#     def __str__(self):
#         return str(self.id)


# class OrderForm(ModelForm):
#     class Meta:
#         model = Order
#         fields = ['first_name', 'last_name',
#                   'address', 'phone', 'city', 'country', 'account', 'files']