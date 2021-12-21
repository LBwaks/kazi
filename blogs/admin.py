from django.contrib import admin
from .models import Blog,Tag
# Register your models here.


class TagAdmin(admin.ModelAdmin):
    list_display=('name','description')
    search_fields=('name','description')

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user= request.user
        obj.save()
        
admin.site.register(Tag,TagAdmin)

class BlogAdmin(admin.ModelAdmin):
    # list_display = ('event_name','event_county','event_location','event_date','created_date','is_featured')
    list_display=('title','tag')
    search_fields=('title','tag')

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user= request.user
        obj.save()

admin.site.register(Blog,BlogAdmin)

# class Blog_CommentAdmin(admin.ModelAdmin):
#     # list_display = ('event_name','event_county','event_location','event_date','created_date','is_featured')
#     list_display=('user','blog')
#     # search_fields=('title','category')
# admin.site.register(Blog_Comment,Blog_CommentAdmin)

