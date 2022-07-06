from django.contrib import admin
from .models import Application
from django.contrib.auth.models import User 



# Register your models here.


class ApplicationAdmin(admin.ModelAdmin):
    list_display=('charge','status','job','created_at','user',)
    search_fields=('status','job')
    list_filter=('created_at','status')

admin.site.register(Application,ApplicationAdmin)