from django.contrib import admin
from .models import Contact

# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    list_display=('name','email','subject','message')
    list_filter=('created_at',)
    search_fields=('name','email','subject','message')
admin.site.register(Contact,ContactAdmin)    