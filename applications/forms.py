from django import forms
from django.core.exceptions import ValidationError
from django.forms import fields, widgets 
from .models import Application, Job
from ckeditor.widgets import CKEditorWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import ( PrependedAppendedText)


class ApplicationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # self.helper=FormHelper()   
        self.helper.layout=Layout(
        PrependedAppendedText('charge','ksh','.00')
        )

    class Meta:
        model = Application 
        fields =('charge',    
            # 'job',     
               'other_description')

        

        labels ={
            'charge':'Charge (ksh)',
            'other_description':'Why Are Charging That Amount'
        }

        widgets ={
            'charge':forms.TextInput(attrs={'class':'form-control' 'required'}),
            'other_description': forms.CharField(widget=CKEditorWidget()),
        }

    def clean(self):
        cleaned_data = super(ApplicationForm,self).clean()
        charge = cleaned_data.get('charge')
        other_description = cleaned_data.get('other_description')

        if len(other_description) < 10 :
            raise ValidationError('Why Are Charging That Amount Should be more than 10 characters !')
        return self.cleaned_data