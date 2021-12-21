from django.shortcuts import render
from applications.forms import ApplicationForm
from applications.models import Application,Job 
from profiles.models import Personal
from django.contrib.auth.models import User
from.forms import ApplicationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse_lazy ,reverse
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,View
from django.shortcuts import render,get_object_or_404 , redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.messages.views import SuccessMessageMixin
from django.utils import timezone
import datetime
# Create your views here.


class ApplicationView(ListView):
    model = Application
    template_name = 'applications/application.html'
    # queryset = Application.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ApplicationView,self).get_context_data(**kwargs)
        job = get_object_or_404(Job,slug=self.kwargs['slug'])
        applications = Application.objects.filter(job=job).order_by('-created_at')
        context={'applications':applications } 
        return context


class JobApplicationsView(ListView):
    model = Application
    template_name = 'applications/this_job_application.html'
    # queryset = Application.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(JobApplicationsView,self).get_context_data(**kwargs)
        job = get_object_or_404(Job,slug=id)
        applications = Application.objects.filter(job=job).order_by('-created_at')
        # applications = Application.objects.get().order_by('-created_at')
        context={'applications':applications } 
        return context
    


class AddApplicationView(SuccessMessageMixin, LoginRequiredMixin,CreateView):
    model =Application
    form_class=ApplicationForm
    template_name ='applications/add_application.html'
    success_message= 'Job Application Successful !'
    # global job 
    # job = Job.objects.get(Job, slug=self.kwargs['slug']) 
    # def get_context_data(self, **kwargs):
    #     context = super(AddApplicationView,self).get_context_data(**kwargs)
    #     application= Application.objects.filter(user=self.request)
    #     context["application"] = application
    #     return context
    
    def form_valid(self,form):        
        # job = get_object_or_404(Job, slug=self.kwargs['slug'])       
        application =form.save(commit=False)
        application.user = self.request.user  
        application.job_id =self.kwargs['job_id']
        # application.job = job.job_id
        application.save()
        # application.save_m2m()
        return super(AddApplicationView,self).form_valid(form)

    # def post(self,slug,**kwargs):
    #     job =get_object_or_404(Job,slug=slug)
    #     form =ApplicationForm
# 
    #     if form.is_valid(self,form):
    #         application = form.save(commit=False)
    #         application.user = self.request.user
    #         application.job= job
    #         application.save()
  

class MyApplicationsView(ListView):
        model = Application
        template_name= 'applications/my_applications.html'

        def get_context_data(self, **kwargs):
            context = super(MyApplicationsView ,self).get_context_data(**kwargs)
            all_applications = Application.objects.filter(user=self.request.user).order_by('-created_at')
            page=self.request.GET.get('page',1)
            paginator =Paginator(all_applications,20)
            try:
                all_applications=paginator.page(page)
            except PageNotAnInteger:
                all_applications=paginator.page(1)
            except EmptyPage:
                all_applications=paginator.page(paginator.num_pages)
            pending_applications = Application.objects.filter(user=self.request.user,status='Pending').order_by('-created_at')
            approved_applications = Application.objects.filter(user=self.request.user,status='Approved').order_by('-created_at')
            cancelled_applications = Application.objects.filter(user=self.request.user,status='Cancelled').order_by('-created_at')
            done_jobs = Application.objects.filter(user=self.request.user,status='Done').order_by('-created_at')
            # context["pending_applications"] = pending_applications
            context={'pending_applications':pending_applications,'all_applications':all_applications,
            'approved_applications':approved_applications,'done_jobs':done_jobs,'cancelled_applications':cancelled_applications}
            return context

def approve_application(request, application_uuid):    
    application = get_object_or_404(Application,application_uuid = application_uuid)    
    application.status='Approved'
    job_id= application.job_id
    application.cancel_reject_done_time=timezone.now() 
    job=get_object_or_404(Job,id=job_id)
    job.status='Approved'
    job.save()  
    application.save()
    if application.save():
        job=get_object_or_404(Job,id=job_id)
        job.status='Approved'
        job.save()
        
    return render(request,'jobs/my_jobs.html')




def cancel_application(request,application_uuid):
    application = get_object_or_404(Application,application_uuid =application_uuid)
   
    application.status='Cancelled'
    application.cancel_reject_done_time=timezone.now()
    application.save()
    return redirect('my_application')


def reject_job(request,application_uuid):
    application = get_object_or_404(Application,application_uuid=application_uuid)
    if application.status =='Approved':
        job_id = application.job_id
        job = get_object_or_404(Job,id=job_id)
        job.status= 'Waiting'
        job.save()
        application.status ='Reject'
        application.cancel_reject_done_time = timezone.now()
    application.status='Rejected'
    application.save()

    return redirect('my_application')

def application_done_job(request,application_uuid):
    application = get_object_or_404(Application,application_uuid=application_uuid)
    if application.status =='Approved':
        job_id = application.job_id
        job = get_object_or_404(Job,id=job_id)
        if job.status == 'Approved' or job.status == ' Done':
            job.status= 'Done'
            job.save()
        application.status ='Done'
        application.cancel_reject_done_time = timezone.now()
    application.status='Done'
    application.save()

    return redirect('my_application')

def ApplicantProfileView(request,username):
    # application=get_object_or_404(Application,application_uuid=application_uuid)
    applicant=get_object_or_404(User,username=username)
    applications = Application.objects.filter(user_id=applicant,status='Done')
    # job_id=applications.job_id
    # jobs =Job.objects.filter(id=job_id)
    return render(request,'profiles/applicant_profile.html',{'username':username,'applicant':applicant,'applications':applications })

