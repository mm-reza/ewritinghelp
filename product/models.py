#pylint: disable=E1101
from django.db import models
from django.utils.html import mark_safe
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.db.models import Avg, Count
# Create your models here.


class Category(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = TreeForeignKey('self', blank=True, null=True,
                            related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(
        blank=True, upload_to='images/', default='images/placeholder.png')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField(null=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    # return self.title

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def image_tag(self):
        if self.image is not None:
            return mark_safe('<img src="/uploads/%s" height="25" width="35"/>' % (self.image))
        else:
            return 'images/placeholder.png'

    # def image_tag(self):
    # return mark_safe('<img src="/uploads/%s" width="50" />' % (self.image))

    image_tag.short_description = 'Image'

    class MPTTMeta:
        order_insertation_by = ['title']

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):                           # __str__ method elaborated later in
        # post.  use __unicode__ in place of
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])


class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )

    VARIANTS = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),

    )
    # many to one relation with Category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = RichTextUploadingField()
    image = models.ImageField(
        upload_to='images/', blank=True, default='images/placeholder.png')
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount = models.IntegerField(default=0)
    minamount = models.IntegerField(default=3)
    variant = models.CharField(max_length=10, choices=VARIANTS, default='None')
    detail = RichTextUploadingField()
    slug = models.SlugField(null=False, unique=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # method to create a fake table field in read only mode

    def image_tag(self):
        if self.image is not None:
            return mark_safe('<img src="/uploads/%s" height="75" width="100">' % (self.image))
        else:
            return 'images/placeholder.png'

    image_tag.short_description = 'Image'
    # def image_tag(self):
    # return mark_safe('<img src="/uploads/%s" width="50" />' % (self.image))

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    # All Product get
    @staticmethod
    def get_all_products():
        return Product.objects.all()

    # Filter Product By Category
    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()

class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(
        blank=True, upload_to='images/', default='images/placeholder.png')

    def __str__(self):
        return self.title

    def image_tag(self):
        if self.image is not None:
            return mark_safe('<img src="/uploads/%s" height="75" width="100">' % (self.image))
        else:
            return 'images/placeholder.png'

    # def image_tag(self):
    # return mark_safe('<img src="/uploads/%s" width="50" />' % (self.image))

    image_tag.short_description = 'Image'


class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250, blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.subject
    
    def image_tag(self):
        if self.image is not None:
            return mark_safe('<img src="/uploads/%s" height="75" width="100">' % (self.image))
        else:
            return ''

    image_tag.short_description = 'Image'

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate', 'image']


class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
        else:
            return ""


class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE,blank=True,null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE,blank=True,null=True)
    image_id = models.IntegerField(blank=True,null=True,default=0)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)

    def __str__(self):
        return self.title
    
    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
             varimage=img.image.url
        else:
            varimage=""
        return varimage

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
             return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""
