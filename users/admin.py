from django.contrib import admin
from.models import  Profile, Comment, Contactus

# Register your models here.
admin.site.register((Profile, Comment, Contactus))

