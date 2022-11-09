#pylint: disable=E1101
from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.forms import ModelForm
from order.models import FOrder
from django.db.models.signals import post_save
from django.dispatch import receiver
from home.validators import validate_file_size

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=50)
    country = models.CharField(blank=True, max_length=50)
    image = models.ImageField(blank=True, upload_to='images/users/')
    email_confirmed = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username       
           
    def username(self):
        return self.user.username

    def email(self):
        return self.user.email

    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + ' [' + self.user.username + '] '

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


class Reply(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    order = models.ForeignKey(FOrder, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    reply = models.CharField(max_length=250, blank=True)
    ip = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    image = models.FileField(upload_to='images/', blank=True, default='images/placeholder.png', validators=[validate_file_size])

    def __str__(self):
        return self.subject
    
    def image_tag(self):
        if self.image is not None:
            return mark_safe('<img src="/uploads/%s" height="40" width="100">' % (self.image))
        else:
            return 'images/placeholder.png'

    image_tag.short_description = 'Image'

class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['subject', 'reply', 'image']