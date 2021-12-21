from django.shortcuts import render
from jobs.models import Job
from .models import Contact 
from applications.models import Application
from django .views.generic import ListView,CreateView,FormView
from jobs.filters import MyJobFilter
from pages.forms import ContactForm, JobSearchForm
from django.contrib.postgres.search import SearchVector
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.messages.views import SuccessMessageMixin
import datetime
import random

# Create your views here.
class HomeView(ListView):
    model =Job
    template_name ='home.html'
    def get_context_data(self, **kwargs):
        context = super(HomeView,self).get_context_data(**kwargs)
        active_jobs = Job.objects.filter(application_deadline__gte=datetime.datetime.now(),status='waiting')
        complete_jobs = Job.objects.filter(application_deadline__gte=datetime.datetime.now(),status='Done')
        applications = Application.objects.filter(status='Pending')
        context["active_jobs"] = active_jobs
        context["complete_jobs"] = complete_jobs
        context['applications']=applications
        return context
    
class ContactView(SuccessMessageMixin, CreateView):
    # model =Contact 
    template_name = 'contact.html'
    form_class = ContactForm
    success_message='Your message has been sent. Thank you!'

    def form_valid(self, form):
        form.send()
        return super().form_valid(form)



def search(request):
    form = JobSearchForm
    results =[]
    
    if 'q' in request.GET:
        form = JobSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            
            results = Job.objects.annotate(search=SearchVector('title','county','location','address','tag'),).filter(search=q).order_by('-created_date')
            page=request.GET.get('page',1)
            paginator = Paginator(results,30)
            try:
                results =paginator.page(page)
            except PageNotAnInteger:
                results=paginator.page(1)
            except EmptyPage:
                results=paginator.page(paginator.num_pages)
            
    return render(request,'pages/search.html',{'form':form,'results':results ,'q':q})