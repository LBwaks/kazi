from django.shortcuts import get_object_or_404, render
from formtools.wizard.views import SessionWizardView
# from formtools.wizard.views import WizardView
from .forms import PersonalForm, LocationForm, SeekerForm,DocumentsForm,EditAccountForm,EditProfileForm
from .models import Personal
from django.core.files.storage import FileSystemStorage
from django.views.generic import DetailView ,CreateView
from allauth.account.views import PasswordChangeView
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import os
from .storage import CustomSessionStorage
from django.urls import reverse_lazy,reverse
from django.contrib.messages.views import SuccessMessageMixin 
from django.views.generic import DetailView ,CreateView,UpdateView
# from .forms import EditProfileForm


# Create your views here.
class Multistepformsubission(SessionWizardView):
    template_name = 'profiles/profile.html'
    form_list = [PersonalForm,LocationForm,SeekerForm,DocumentsForm]
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'users'))
        
    def done(self, form_list,form_dict, **kwargs):
        storage_name = CustomSessionStorage.storage_path
        form_data= [form.cleaned_data for form in form_list]
        form_dict = self.get_all_cleaned_data()
        
        personal = Personal.objects.create(**form_dict,user=self.request.user,)
        personal.save()
       
        return render(self.request, 'home.html', {
            'data':form_data
        })

class MyProfileView(LoginRequiredMixin,DetailView):
    model = Personal
    template_name = 'profiles/my_profile.html'
    slug_url_kwarg ='profile_uuid'
    slug_field = "profile_uuid"

    def get_context_data(self, **kwargs):
        context = super(MyProfileView,self).get_context_data(**kwargs)
        my_profile = get_object_or_404(Personal,profile_uuid=self.kwargs['profile_uuid'])
        context["my_profile"] = my_profile 
        return context
    
class EditProfileView(UpdateView):
    model= Personal
    template_name = 'profiles/edit_profile.html'
    slug_url_kwarg = "profile_uuid"
    slug_field = "profile_uuid"    
    form_class = EditProfileForm    
    def form_valid(self, form):      
       form.instance.user = self.request.user      
       return super().form_valid(form)
    # success_url = reverse_lazy('profile') 


class EditAccountView(UpdateView): 

    template_name = 'profiles/edit_account.html'
    form_class = EditAccountForm
    slug_url_kwarg = "profile_uuid"
    slug_field = "profile_uuid"   
    
    success_url =reverse_lazy('home' )
    
    

    def get_object(self):
        return self.request.user
class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('home')


