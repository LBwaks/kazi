from django import forms 
from .models import Contact
from django.conf import settings
from django.core.mail import send_mail
# from pages.tasks import contact_email_task

class JobSearchForm(forms.Form):
    q = forms.CharField()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['q'].label='Search For'
        self.fields['q'].widget.attrs.update({'class':'form-control'})

class ContactForm(forms.ModelForm):
    class  Meta :
        model = Contact
        fields = '__all__'
    def get_info(self):

        cleaned_data = super(ContactForm,self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        subject = cleaned_data.get('subject')
        # message = cleaned_data.get('message')

        message =f'{name} with email {email} said:'
        message += f'\n"{subject}"\n\n'
        message += cleaned_data.get('message')

        return subject , message

    def send(self):
        subject, message = self.get_info()
        send_mail(
            subject = subject,
            message = message,
            from_email = settings.EMAIL_HOST_USER,
            recipient_list=[settings.RECIPIENT_ADDRESS]
        )        

    # def send_email(self):
    #     contact_email_task.delay(subject=self.get_info(), message = self.get_info())
