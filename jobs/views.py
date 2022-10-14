from datetime import datetime
from django import template
from django.core.checks import messages
from django.dispatch.dispatcher import receiver
from django.shortcuts import get_object_or_404, redirect, render
from django .views.generic import ListView,DetailView,CreateView,UpdateView
from django.http import HttpResponseRedirect,FileResponse,HttpResponse, response
from django.views import View
from django.forms.models import modelformset_factory 
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import DeleteView
from applications.models import Application
from jobs.forms import JobForm ,JobEditForm, JobSearchForm
from pages.forms import JobSearchForm
from .models import Job,Tag,JobImage
from django.contrib.auth.models import User
from django.urls.base import reverse_lazy,reverse
from django.db import transaction
from django.utils import timezone
import datetime
# from reportlab.pdfgen import canvas
# import io
from django.template.loader import get_template
from xhtml2pdf import pisa
# Create your views here.

class JobView(ListView):
    model = Job 
    template_name ='jobs/jobs.html'
    paginate_by = 16
    
    def get_queryset(self):
        
        queryset=Job.objects.filter(application_deadline__gte=datetime.datetime.now(),status='waiting').order_by('-created_date')
        return queryset
    
# application_deadline__gte=datetime.datetime.now(),status='waiting'
   
class JobDetailView(DetailView):
    model =Job 
    template_name ='jobs/job-details.html'
    form =JobSearchForm
    
    def get_related_job_by_tag(self):
        return Job.objects.filter(application_deadline__gte=datetime.datetime.now(),status='waiting',tag_slug=self.tag_slug).exclude(slug=self.slug).order_by('-created_date')[:8]

    def get_context_data(self,*args, **kwargs):
        context= super(JobDetailView,self).get_context_data(**kwargs)
        job = get_object_or_404(Job,slug=self.kwargs['slug'])
        # applications= Application.objects.filter(job=job).first()
        context['job'] =job
        # context['applications'] = applications
        return context

class AddJobView(SuccessMessageMixin,LoginRequiredMixin,CreateView):
    
    form_class = JobForm
    template_name = 'jobs/add_jobs.html'
    success_message ='Job Posted Successfully !'


  

    def form_valid(self,form):
        images =self.request.FILES.getlist('job_images')        
        job =form.save(commit=False)
        job.user = self.request.user
        # self.object =form.save()        
        job.save()
        
        for image in images:
              JobImage.objects.create(job=job,image=image)
        return super(AddJobView,self).form_valid(form)
    
          

class UpdateJobView(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    model =Job 
    form_class=JobEditForm
    template_name ='jobs/update_job.html'
    success_message ='Job Edited Successfully !'

    def form_valid(self,form):
        images =self.request.FILES.getlist('job_images')        
        job =form.save(commit=False)              
        job.save()
        
        for image in images:
              JobImage.objects.create(job=job,image=image)
        return super(UpdateJobView,self).form_valid(form)

class DeleteJobView(SuccessMessageMixin,LoginRequiredMixin,DeleteView):
    model= Job
    template_name ='jobs/delete_job.html'
    success_url =reverse_lazy('jobs')
    success_message ='Job Deleted Successfully !'

# class JobApplicationView(ListView):
#     model = Job 
#     template_name ='applications/applications.html'

#     def  get_context_data(self, **kwargs):
#         context = super(JobApplicationView,self).get_context_data(**kwargs)
#         job = get_object_or_404(Job,slug=self.kwargs['slug'])
#         applications= Application.objects.filter(job=job).order_by('created_at')
#         context["applications"] = applications
#         return context
    
class JobApplicationsView(ListView):
    model = Job
    template_name = 'applications/this_job_application.html'
    # queryset = Application.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(JobApplicationsView,self).get_context_data(**kwargs)
        job = get_object_or_404(Job,slug=self.kwargs['slug'])
        applications = Application.objects.filter(job=job)
        job_has_approved_application=Application.objects.filter(job=job,status ='Approved')
        job_has_done_status=Application.objects.filter(job=job,status ='Done')
        # .order_by('-created_at')
        # applications = Application.objects.get().order_by('-created_at')
        context['applications']=applications
        context['job_has_approved_application']=job_has_approved_application
        context['job_has_done_status']=job_has_done_status
        context['job']=job
        return context
        
class Search(ListView):
    model = Job
    template_name= 'pages/search.html'


class MyJobsView(ListView):
    model = Job
    template_name = 'jobs/my_jobs.html'
   
    def get_context_data(self, **kwargs):
        context = super(MyJobsView,self).get_context_data(**kwargs)       
       

        approved_jobs = Job.objects.filter(user = self.request.user,status='Approved').order_by('-created_date')       
        waiting_jobs = Job.objects.filter(user = self.request.user,status='waiting').order_by('-created_date')

        never_applied_jobs = Job.objects.filter(user=self.request.user,application_deadline__lte=datetime.datetime.now(),status='waiting' ).order_by('-created_date')

        done_jobs = Job.objects.filter(user = self.request.user,status='Done').order_by('-created_date')

        context = {
            'approved_jobs':approved_jobs,'waiting_jobs':waiting_jobs, 'never_applied_jobs':never_applied_jobs,'done_jobs':done_jobs
            }
        return context

    
def approve_application(request, application_uuid):    
    application = get_object_or_404(Application,application_uuid = application_uuid)  
    applicant_id= application.user_id 
    applicant = get_object_or_404(User,id=applicant_id)
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
        messages.add_message(request,messages.SUCCESS,'Application Approved Successfully !')

    # if application.save() and job.save():
    #     sender = User.objects.get(username=request.user)
    #     receiver = applicant
    #     notify.send(sender,recipient=receiver,verb='Message',description="Approved")

    return redirect("this_job_applications", slug=job.slug,)

def cancel(request,application_uuid):
    application = get_object_or_404(Application,application_uuid =application_uuid)
    if application.status=='Approved':
        job_id = application.job_id
        job = get_object_or_404(Job, id=job_id)
        job.status ='Waiting'
        job.save()
        application.status='Cancelled'        
        application.cancel_reject_done_time=timezone.now()
    application.save()
    if application.save():
        job=get_object_or_404(Job,id=job_id)
        job.status='Waiting'
        job.save()
        messages.add_message(request,messages.SUCCESS,'Application Approved Successfully !')

    # return render(request,'applications/this_job_application.html')
    return redirect("this_job_applications", slug=job.slug)


def done_job(request,application_uuid):
    application = get_object_or_404(Application,application_uuid=application_uuid)
    if application.status =='Approved':
        job_id = application.job_id
        job =get_object_or_404(Job,id=job_id)
        job.status= 'Done'
        job.save()
        application.status ='Done'
        application.cancel_reject_done_time = timezone.now()
    application.status='Done'
    application.save()   
    return render(request,'applications/done_job.html',{'application':application})

def get_done_page(request,application_uuid):
    application=get_object_or_404(Application,application_uuid=application_uuid)
    return render(request,'applications/done_job.html',{'application':application})

# def get_invoice(request):
#     # application = get_object_or_404(Application,application_uuid=application_uuid)
#     buffer =io.BytesIO()
#     p =canvas.Canvas(buffer)
#     p.drawString(100,100,"Hello World")
#     p.showPage()
#     p.save()
#     buffer.seek(0)
#     return FileResponse(buffer,as_attachment=True,filename='hello.pdf')

def pdf(request,application_uuid):
    application = get_object_or_404(Application,application_uuid=application_uuid)
    template_path= 'pdf/invoice.html'
    context={'application':application}
    response=HttpResponse(content_type="application/pdf")
    response['Comtent-Diposition']='attachment;filename="invoice.pdf"'
    template=get_template(template_path)
    html = template.render(context)
    pisa_status =pisa.CreatePDF(
        html,dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '<pre>')
    return response


def TagView(request,slug):
    tags=get_object_or_404(Tag,slug=slug)
    jobs=Job.objects.filter(tag=tags,application_deadline__gte=datetime.datetime.now(),status='waiting').order_by('created_date')
    
    page=request.GET.get('page',1)
    paginator = Paginator(jobs,16)
    try:
        jobs =paginator.page(page)
    except PageNotAnInteger:
        jobs=paginator.page(1)
    except EmptyPage:
        jobs=paginator.page(paginator.num_pages)
    return render(request,'tags/tags.html',{'slug':slug,'jobs':jobs,'tags':tags})

def UserView(request,username):
    jobs_by=get_object_or_404(User,username=username)
    jobs=Job.objects.filter(user=jobs_by,application_deadline__gte=datetime.datetime.now(),status='waiting')
    page=request.GET.get('page',1)
    paginator =Paginator(jobs,16)
    try:
        jobs=paginator.page(page)
    except PageNotAnInteger:
        jobs=paginator.page(1)
    except EmptyPage:
        jobs=paginator.page(paginator.num_pages)
    return render(request,'users/users.html',{'username':username,'jobs_by':jobs_by,'jobs':jobs})
    


    






