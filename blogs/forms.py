from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from .models import Blog,Blog_Comment
from ckeditor.widgets import CKEditorWidget
from blogs import validators
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields =('title','tag','description','photo')
        labels={
            'title':'Blog Title',
            'tag':'Blog Tag',
            'description':'About The Blog',
            'photo':'Blog Image'
        }

        widgets={
            'title': forms.TextInput(attrs={'class':'form-control title ' 'required'}),
            'tag': forms.Select(attrs={'class':'form-select tag '}),
            'description': forms.CharField(widget=CKEditorWidget(attrs={'class':'description '})),
            'photo': forms.FileInput(attrs={'class':'form-control photo ','multiple':True,}),
         
        }

    def clean(self):
        cleaned_data = super(BlogForm,self).clean()
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        if len(title) < 10 :
            raise ValidationError('Title Should Contain A Minimum of 10 Characters')
        if len(description) < 30:
            raise ValidationError('Description Should Contain 30 Characters')     
        return self.cleaned_data

    def clean_photo(self):
        # if photo != None:
            photo = self.cleaned_data['photo']
            content_type = photo.content_type.split('/')[0]
            if content_type in settings.CONTENT_TYPES:
                if photo.size > int(settings.MAX_IMAGE_UPLOAD_SIZE):
                    raise forms.ValidationError(_(u'Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_IMAGE_UPLOAD_SIZE), filesizeformat(photo.size)))
            else:
                raise forms.ValidationError(_(u'File type is not supported'))
            return photo  

class EditBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields =('title','tag','description','photo')
        labels={
            'title':'Blog Title',
            'tag':'Blog Tag',
            'description':'About The Blog',
            'photo':'Blog Image'
        }

        widgets={
            'title': forms.TextInput(attrs={'class':'form-control title ' 'required'}),
            'tag': forms.Select(attrs={'class':'form-select tag '}),
            'description': forms.CharField(widget=CKEditorWidget(attrs={'class':'description '})),
            'photo': forms.FileInput(attrs={'class':'form-control photo ','multiple':True,}),
         
         
        }
    def clean(self):
        cleaned_data = super(EditBlogForm,self).clean()
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        if len(title) < 10 :
            raise ValidationError('Title Should Contain A Minimum of 10 Characters')
        if len(description) < 30:
            raise ValidationError('Description Should Contain 30 Characters')     
        return self.cleaned_data

   
    def clean_photo(self):
        photo = self.cleaned_data.get('photo', False)
        
        if photo:
            if photo.size > 1*1024*1024:
                raise ValidationError("Image file too large ( > 5mb )")
            return photo
        else:
            raise ValidationError("Couldn't read uploaded image")
            

class CommentForm(forms.ModelForm):
    class Meta:
        model = Blog_Comment
        fields = ('body',)
        labels={
            'body':'Comment',
        }
        widgets={
            'body':forms.CharField(widget=CKEditorWidget()
            )
        }
        def clean(self):
            cleaned_data = super(CommentForm,self).clean()
            body = cleaned_data.get('body')
            