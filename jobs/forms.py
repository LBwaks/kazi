from autoslug import fields
from django import forms
from django.forms import widgets
from django.forms.models import inlineformset_factory 
from .models import Job, JobImage
from ckeditor.widgets import CKEditorWidget
import datetime
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from jobs import validators
class JobForm(forms.ModelForm):
    # image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    job_images= forms.FileField(required=True,widget=forms.FileInput(attrs={
        'required'
        'class':'form-control images',
        'multiple' : True 
        
    }))
    class Meta:
        model =Job
        fields =('title','tag','description',
        'application_deadline','job_done_date',
        'county',
        'location',
        'address',
        # 'image',
        # 'video'
        )      

        labels ={
            'title':'Job Title ',
            'tag': 'Job Tag ',
            'description':'Job Description ',            
            'application_deadline': 'Application Deadline ',
            'job_done_date': 'Job To Be Done At ',
            'county': 'County ',
            'address': 'Estate',
            'location': 'Town/City',
            'job_images': 'Job Image ',
            # 'video':'Job Video ',
        }

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control title ' 'required'}),
            'tag': forms.Select(attrs={'class':'form-select'}),
            'description': forms.CharField(widget=CKEditorWidget(attrs={'class':'description '})),
            'application_deadline': forms.DateInput(format=('%Y-%m-%d %H:%M'), attrs={'class': 'form-control application_deadline ','placeholder': 'Select a date','type': 'datetime-local' }),
            'job_done_date': forms.DateInput(format=('%Y-%m-%d %H:%M'), attrs={'class': 'form-control job_done_date ','placeholder ': 'Select a date','type': 'datetime-local' }),
            'county': forms.Select(attrs={'class':'form-select county ' 'required'}),
            'location': forms.TextInput(attrs={'class':'form-control location ' 'required'}),
            'address': forms.TextInput(attrs={'class':'form-control address ' 'required'}),
            # 'image': forms.ClearableFileInput(attrs={'class':'form-control image ','multiple':True}),
            # 'video':forms.FileInput(attrs={'class':'form-control video '}),
        }
        

        # def clean_title(self):
        #     data = self.cleaned_data["title"]
        #     if len(data) < 5:
        #         raise forms.ValidationError('Title should contain a minimum of 10 characters ')
            
        #     return data
########################################################################################################
#          VALID_IMAGE_EXTENSIONS = [
#     ".jpg",
#     ".jpeg",
#     ".png",
#     ".gif",
# ]

    def clean(self):
            cleaned_data = super(JobForm, self).clean()

            title = cleaned_data.get('title')
            description = cleaned_data.get('description')
            application_deadline = cleaned_data.get('application_deadline')
            job_done_date = cleaned_data.get('job_done_date')
            county = cleaned_data.get('county')
            location = cleaned_data.get('location')
            address = cleaned_data.get('address')
            
            if len(title) < 10:
                raise ValidationError('Title should contain a minimum of 10 characters ')

            if len(description) < 30:
                raise ValidationError('Description should contain a minimum of 30 characters ')
            if application_deadline.date() < datetime.date.today():
                raise ValidationError('Application  Deadline Should Be Greater Than The Current Time ! ')
            if job_done_date.date() < datetime.date.today():
                raise ValidationError('Time Job To be Done  Should Be Greater Than The Current Time !  ')
            if job_done_date < application_deadline:  
                raise ValidationError('Application Date  Cannot be less than Job Done Date!')
            if len(location) < 3:
                raise ValidationError('Location should contain a minimum of 3 characters')
            if len(address) < 3:
                raise ValidationError('Address should contain a minimum of 3 characters')    

            return self.cleaned_data


    def clean_image(self):
        job_images = self.cleaned_data.get('image', False)
        if job_images == 'jobs/job_images/jobs.jpg':
            pass
        elif job_images:
            if job_images.size > 5*1024*1024:
                raise ValidationError("Image file too large ( > 4mb )")
            return job_images
        else:
            raise ValidationError("Couldn't read uploaded image")
            
    def clean_video(self):
        video = self.cleaned_data['video']
        if video != None:
            video = self.cleaned_data['video']
            content_type = video.content_type.split('/')[0]
            if content_type in settings.CONTENT_TYPES:
                if video.size > int(settings.MAX_JOB_VIDEO_UPLOAD_SIZE):
                    raise forms.ValidationError(_(u'Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_JOB_VIDEO_UPLOAD_SIZE), filesizeformat(video.size)))
            else:
                raise forms.ValidationError(_(u'File type is not supported'))
            return video   


class JobEditForm(forms.ModelForm):
    job_images= forms.FileField(required=True,widget=forms.FileInput(attrs={
        'required'
        'class':'form-control images',
        'multiple' : True 
        
    }))
    class Meta:
        model =Job
        fields =('title','tag','description',
        'application_deadline','job_done_date',
        'county',
        'location',
        'address',
        # 'image','video'
        )

        labels ={
            'title':'Job Title ',
            'tag': 'Job Tag ',
            'description':'Job Description ',            
            'application_deadline': 'Job Done By Date ',
            'job_done_date': 'Job To Be Done At  ',
            'county': 'County ',
            'location': 'Location ',            
            'address': 'Address ',
            'job_images': 'Job Image ',
            # 'video':'Job Video ',
        }

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control title ' 'required'}),
            'tag': forms.Select(attrs={'class':'form-select'}),
            'description': forms.CharField(widget=CKEditorWidget(attrs={'class':'description '})),
            'application_deadline': forms.DateInput(format=('%Y-%m-%d %H:%M'), attrs={'class': 'form-control application_deadline ','type': 'datetime-local' }),
            'job_done_date': forms.DateInput(format=('%Y-%m-%d %H:%M'), attrs={'class': 'form-control job_done_date ','type': 'datetime-local' }),
            'county': forms.Select(attrs={'class':'form-select county ' 'required'}),
            'location': forms.TextInput(attrs={'class':'form-control location ' 'required'}),
            'address': forms.TextInput(attrs={'class':'form-control address ' 'required'}),
            # 'image': forms.FileInput(attrs={'class':'form-control image ','multiple':True}),
            # 'video':forms.FileInput(attrs={'class':'form-control video '}),
       }
    def clean(self):
            cleaned_data = super(JobEditForm, self).clean()

            title = cleaned_data.get('title')
            description = cleaned_data.get('description')
            application_deadline = cleaned_data.get('application_deadline')
            job_done_date = cleaned_data.get('job_done_date')
            county = cleaned_data.get('county')
            location = cleaned_data.get('location')
            address = cleaned_data.get('address')
            
            if len(title) < 10:
                raise ValidationError('Title should contain a minimum of 10 characters ')

            if len(description) < 30:
                raise ValidationError('Description should contain a minimum of 30 characters ')
            if application_deadline.date() < datetime.date.today():
                raise ValidationError('Application  Deadline Should Be Greater Than The Current Time ! ')
            if job_done_date.date() < datetime.date.today():
                raise ValidationError('Time Job To be Done  Should Be Greater Than The Current Time !  ')
            if job_done_date < application_deadline:  
                raise ValidationError('Application Date  Cannot be less than Job Done Date!')
            if len(location) < 3:
                raise ValidationError('Location should contain a minimum of 3 characters')
            if len(address) < 3:
                raise ValidationError('Address should contain a minimum of 3 characters')    

            return self.cleaned_data

    def clean_image(self):
        job_images = self.cleaned_data.get('image', False)
        if job_images == 'jobs/job_images/jobs.jpg':
            pass
        elif job_images:
            if job_images.size > 5*1024*1024:
                raise ValidationError("Image file too large ( > 5mb )")
            return job_images
        else:
            raise ValidationError("Couldn't read uploaded image")
            
    
    def clean_video(self):
        video = self.cleaned_data.get('video', False)
        if video == 'jobs/job_images/jobs.jpg':
            pass
        elif video:
            if video.size > 10*1024*1024:
                raise ValidationError("Video file too large ( > 10mb )")
            return video
        else:
            raise ValidationError("Couldn't read uploaded Video")
            

class JobSearchForm(forms.Form):
    q = forms.CharField()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['q'].label='Search For'
        self.fields['q'].widget.attrs.update({'class':'form-control'})
