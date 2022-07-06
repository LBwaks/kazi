from django.contrib import admin
from .models import Job ,Category,Tag
from django.contrib.auth.models import User 
from django.utils.html import format_html

class JobAdmin(admin.ModelAdmin):
    def ImageThumbnail(self,object):
        return format_html('<img src ="{}" width = "60" class="img-thumbail"/>'.format(object.image.url))
    ImageThumbnail.short_description = 'Job Image'
    list_display = ('title','tag','county', 'location','is_featured','created_date')
    search_fields=('title','county','location','address','description')
    list_editable=('is_featured',)
    list_filter=('application_deadline','created_date','status')
    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user= request.user
        obj.save()
admin.site.register(Job,JobAdmin)

class CategoryAdmin(admin.ModelAdmin):
   
    list_display =  ('name','description','created_date')    
    search_fields=('name',)
    list_filter= ('created_date',)

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user= request.user
        obj.save()
    
admin.site.register(Category,CategoryAdmin)

class TagAdmin(admin.ModelAdmin):  

    list_display =  ('name','description','created_date')    
    search_fields=('name',)
    list_filter= ('category','created_date')

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user= request.user
        obj.save()
    
admin.site.register(Tag,TagAdmin)

# Register your models here.
