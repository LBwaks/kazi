from django import forms
from .models import Personal
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.forms import PasswordChangeForm,  UserCreationForm ,UserChangeForm
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class PersonalForm(forms.ModelForm):
    class Meta :
        model = Personal
        fields = ('user_type','phone_number','id_passport','gender','bio','profile_pic')
        labels= {
            'user_type':'Type Of The User',
            'phone_number':'Phone Number',
            'id_passport':'ID / Passport Number',
            'gender':'Gender',
            'bio':'Short Bio',
            'profile_pic' : 'Profile Image'
        }

def clean(self):
    cleaned_data = super(PersonalForm,self).clean()
    id_passport = cleaned_data.get('id_passport')
    bio = cleaned_data.get('bio')

    if len(id_passport) < 8 or len(id_passport) > 12 :
        raise ValidationError('ID should have 8 characters Or Passport should have 12 Characters !')
    return self.cleaned_data

def profile_pic(self):
        profile_pic = self.cleaned_data.get('profile_pic', False)
        if profile_pic == 'users/profile/user_0/profile.png':
            pass
        elif profile_pic:
            if profile_pic.size > 5*1024*1024:
                raise ValidationError("Profile Picture file too large ( > 5mb )")
            return profile_pic
        else:
            raise ValidationError("Couldn't read uploaded Profile Picture")
                


class LocationForm(forms.ModelForm):
    class Meta :
        model = Personal
        fields = ('county','location','address',)
        labels ={
            'county':'County',
            'address':'Address',
            'location':'Location/Town',
            
        }
    def clean(self):
        cleaned_data = super(LocationForm,self).clean()
        address = cleaned_data.get('address')
        location = cleaned_data.get('location')

        return self.cleaned_data

class SeekerForm(forms.ModelForm):
    class Meta :
        model = Personal
        fields =('skills',)
        labels= {
           'skills':'What are your skills : ( For Job Seekers Only ) '
        }
        widgets = {
            'skills': forms.TextInput(attrs={'class':'form-control','placeholder': 'For Job Seekers Only',}),
        }
    def clean(self):
        cleaned_data = super(SeekerForm,self).clean()
        skills = cleaned_data.get('skills')

        return self.cleaned_data
class DocumentsForm(forms.ModelForm):
    class Meta :
        model = Personal
        fields =('cv','id_front','id_back')
        labels = {
            'cv':'Curriculum Vitae : ( For Job Seekers Only )',            
            'id_front':'Front Side of ID / Passport : ( For Job Seekers Only )',
            'id_back':'Back Side of ID / Passport : ( For Job Seekers Only )',
        }

    def profile_pic(self):
        profile_pic = self.cleaned_data.get('profile_pic', False)
        if profile_pic == 'users/profile/user_0/profile.png':
            pass
        elif profile_pic:
            if profile_pic.size > 5*1024*1024:
                raise ValidationError("Profile Picture file too large ( > 5mb )")
            return profile_pic
        else:
            raise ValidationError("Couldn't read uploaded Profile Picture")

    def profile_pic(self):
        profile_pic = self.cleaned_data.get('profile_pic', False)
        if profile_pic == 'users/profile/user_0/profile.png':
            pass
        elif profile_pic:
            if profile_pic.size > 5*1024*1024:
                raise ValidationError("Profile Picture file too large ( > 5mb )")
            return profile_pic
        else:
            raise ValidationError("Couldn't read uploaded Profile Picture")

    def profile_pic(self):
        profile_pic = self.cleaned_data.get('profile_pic', False)
        if profile_pic == 'users/profile/user_0/profile.png':
            pass
        elif profile_pic:
            if profile_pic.size > 5*1024*1024:
                raise ValidationError("Profile Picture file too large ( > 5mb )")
            return profile_pic
        else:
            raise ValidationError("Couldn't read uploaded Profile Picture")
                                         
    def clean_id_front(self):
        # if id_front != None:
            id_front = self.cleaned_data['id_front']
            content_type = id_front.content_type.split('/')[0]
            if content_type in settings.CONTENT_TYPES:
                if id_front.size > int(settings.MAX_IMAGE_UPLOAD_SIZE):
                    raise forms.ValidationError(_(u'Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_IMAGE_UPLOAD_SIZE), filesizeformat(id_front.size)))
            else:
                raise forms.ValidationError(_(u'File type is not supported'))
            return id_front 
    def clean_id_back(self):
        # if id_back != None:
            id_back = self.cleaned_data['id_back']
            content_type = id_back.content_type.split('/')[0]
            if content_type in settings.CONTENT_TYPES:
                if id_back.size > int(settings.MAX_IMAGE_UPLOAD_SIZE):
                    raise forms.ValidationError(_(u'Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_IMAGE_UPLOAD_SIZE), filesizeformat(id_back.size)))
            else:
                raise forms.ValidationError(_(u'File type is not supported'))
            return id_back  

    def clean_cv(self):
        # if cv != None:
            cv = self.cleaned_data['cv']
            content_type = cv.content_type.split('/')[0]
            if content_type in settings.CONTENT_TYPES:
                if cv.size > int(settings.MAX_IMAGE_UPLOAD_SIZE):
                    raise forms.ValidationError(_(u'Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_IMAGE_UPLOAD_SIZE), filesizeformat(cv.size)))
            else:
                raise forms.ValidationError(_(u'File type is not supported'))
            return cv          

class EditProfileForm(forms.ModelForm):
    class Meta :
        model = Personal 
        fields =('user_type','phone_number','id_passport','gender','bio','profile_pic',
        'county','location','address',
        'skills','cv',)

        labels= {
            'user_type':'Type Of The User',
            'phone_number':'Phone Number',
            'id_passport':'ID / Passport Number',
            'gender':'Gender',
            'bio':'Short Bio',
            'profile_pic' : 'Profile Image',
            'county':'County',
            'address':'Address',
            'location':'Town/Location',            
            'skills':'What are your skills : ( For Job Seekers Only ) ',
            'cv':' Curriculum Vitae : ( For Job Seekers Only )',
           
        }

        widgets = {
            'skills': forms.TextInput(attrs={'class':'form-control','placeholder': 'For Job Seekers Only',}),
        }
    def clean(self):
        cleaned_data = super(EditProfileForm,self).clean()
        id_passport = cleaned_data.get('id_passport')
        bio = cleaned_data.get('bio')
        address = cleaned_data.get('address')
        location = cleaned_data.get('location')
        skills = cleaned_data.get('skills')



        if len(id_passport) < 8 or len(id_passport) > 12 :
            raise ValidationError('ID should have 8 characters Or Passport should have 12 Characters !')
        return self.cleaned_data

    # def clean_profile_pic(self):
    #     # if profile_pic != None:
    #         profile = self.cleaned_data['profile_pic']
    #         content_type = profile.content_type.split('/')[0]
    #         if content_type in settings.CONTENT_TYPES:
    #             if profile.size > int(settings.MAX_IMAGE_UPLOAD_SIZE):
    #                 raise forms.ValidationError(_(u'Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_IMAGE_UPLOAD_SIZE), filesizeformat(profile.size)))
    #         else:
    #             raise forms.ValidationError(_(u'File type is not supported'))
    #         return profile   
    
    def profile_pic(self):
        profile_pic = self.cleaned_data.get('profile_pic', False)
        # if profile_pic == 'users/profile/user_0/profile.png':
        #     pass
        if profile_pic:
            if profile_pic.size > 5*1024*1024:
                raise ValidationError("Profile Picture file too large ( > 5mb )")
            return profile_pic
        else:
            raise ValidationError("Couldn't read uploaded Profile Picture")

    def clean_id_front(self):
        # if id_front != None:
            id_front = self.cleaned_data['id_front']
            content_type = id_front.content_type.split('/')[0]
            if content_type in settings.CONTENT_TYPES:
                if id_front.size > int(settings.MAX_IMAGE_UPLOAD_SIZE):
                    raise forms.ValidationError(_(u'Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_IMAGE_UPLOAD_SIZE), filesizeformat(id_front.size)))
            else:
                raise forms.ValidationError(_(u'File type is not supported'))
            return id_front 
    def clean_id_back(self):
        # if id_back != None:
            id_back = self.cleaned_data['id_back']
            content_type = id_back.content_type.split('/')[0]
            if content_type in settings.CONTENT_TYPES:
                if id_back.size > int(settings.MAX_IMAGE_UPLOAD_SIZE):
                    raise forms.ValidationError(_(u'Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_IMAGE_UPLOAD_SIZE), filesizeformat(id_back.size)))
            else:
                raise forms.ValidationError(_(u'File type is not supported'))
            return id_back  

           
    def clean_cv(self):
        cv = self.cleaned_data.get('cv', False)
        # if cv == None:
        #     pass
        if cv:
            if cv.size > 5*1024*1024:
                raise ValidationError("Profile Picture file too large ( > 5mb )")
            return cv
        else:
            raise ValidationError("Couldn't read uploaded Profile Picture")

class EditAccountForm(UserChangeForm):
    password=None
    
    class Meta:
        model = User
        
        fields =( 'username','first_name','last_name','email')
        # exclude = ['password']
        help_texts = {
            'password': None,
            
        }
#    A001898943P
#    2061583