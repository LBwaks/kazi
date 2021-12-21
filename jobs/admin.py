from django.contrib import admin
from .models import Job ,Category,Tag
from django.contrib.auth.models import User 
from django.utils.html import format_html

class JobAdmin(admin.ModelAdmin):
    def ImageThumbail(self,object):
        return format_html('<img src ="{}" width = "60" class="img-thumbail"/>'.format(object.photo.url))
    ImageThumbail.short_description = 'Job Image'
    list_display = ('title','tag','created_date')
    search_fields=('title',)
    # def save_model(self, request, obj, form, change):
    #     if not obj.user_id:
    #         obj.user= request.user
    #     obj.save()
admin.site.register(Job,JobAdmin)

class CategoryAdmin(admin.ModelAdmin):
    # def ImageThumbnail(self,object):
    #     return format_html('<img src="{}" width="60" class="img-thumbnail"/>'.format(object.photo.url))
    # ImageThumbnail.short_description='Event Poster'


    list_display =  ('name','description','created_date')
    
    search_fields=('name',)
    list_filter= ('name','created_date')

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user= request.user
        obj.save()
    
admin.site.register(Category,CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    # def ImageThumbnail(self,object):
    #     return format_html('<img src="{}" width="60" class="img-thumbnail"/>'.format(object.photo.url))
    # ImageThumbnail.short_description='Event Poster'


    list_display =  ('name','description','created_date')
    
    search_fields=('name',)
    list_filter= ('name','created_date')

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user= request.user
        obj.save()
    
admin.site.register(Tag,TagAdmin)

# Register your models here.
