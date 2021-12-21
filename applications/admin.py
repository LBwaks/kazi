from django.contrib import admin
from .models import Application
from django.contrib.auth.models import User 


# Register your models here.


class ApplicationAdmin(admin.ModelAdmin):
    list_display=('user','job','charge','status')

admin.site.register(Application,ApplicationAdmin)