from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm, TextInput, FileInput, Select
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from product.models import Category


class Menu(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=100,unique=True)
    link = models.CharField(blank=True, max_length=100)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return '->'.join(full_path[::-1])

class Content(models.Model):
    TYPE = (
        ('Menu', 'Menu'),
        ('TarihiYerler', 'TarihiYerler'),
        ('Muzeler', 'Muzeler'),
        ('TatilBeldeleri', 'TatilBeldeleri'),
    )

    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    menu = models.ForeignKey(Menu, blank=True, null=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE)
    title = models.CharField(max_length=150)
    description = models.CharField(blank=True, max_length=255)
    keywords = models.CharField(blank=True, max_length=255)
    status = models.CharField(max_length=10, choices=STATUS)
    image = models.ImageField(blank=True, upload_to='images/')
    detail = RichTextUploadingField()
    slug = models.SlugField(null=False, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'
    def get_absolute_url(self):
        return reverse('content_detail', kwargs={'slug':self.slug})

class CImages(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

class ContentImageForm(ModelForm):
    class Meta:
        model = CImages
        fields =['title', 'image']

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

class Ccomment(models.Model):
    STATUS = (
        ('New', 'Yeni'),
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(blank=True,max_length=50)
    comment = models.CharField(blank=True, max_length=200)
    rate = models.IntegerField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS,default='New')
    ip = models.CharField(blank=True, max_length=20)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class CcommentForm(ModelForm):
    class Meta:
        model = Ccomment
        fields = ['subject','comment','rate']


TYPE = (
        ('Menu', 'Menu'),
        ('TarihiYerler', 'TarihiYerler'),
        ('Muzeler', 'Muzeler'),
        ('TatilBeldeleri', 'TatilBeldeleri'),
    )
class ContentForm(ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'slug', 'keywords', 'description','type', 'category', 'image', 'detail']

    widgets = {
        'title'      : TextInput(attrs={'class': 'input', 'placeholder': 'title'}),
        'slug'       : TextInput(attrs={'class': 'input', 'placeholder': 'slug'}),
        'keywords'   : TextInput(attrs={'class': 'input', 'placeholder': 'keywords'}),
        'description': TextInput(attrs={'class': 'input', 'placeholder': 'description'}),
        'type'       : Select(attrs={'class': 'input', 'placeholder': 'type'}, choices=TYPE),
        'category': TextInput(attrs={'class': 'input', 'placeholder': 'category'}),
        'image'      : FileInput(attrs={'class': 'input', 'placeholder': 'image'}),
        'detail'     : CKEditorWidget(),
    }


