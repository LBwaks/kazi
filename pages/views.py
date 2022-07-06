from django.shortcuts import get_object_or_404, render
from jobs.models import Job,Tag
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
        tags=Tag.objects.all()
        context["active_jobs"] = active_jobs
        context["complete_jobs"] = complete_jobs
        context['applications']=applications
        context['tags']=tags
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
    
    if request.method == 'GET':
        
            tag= request.GET.get('tag',None)
            title=request.GET.get('title')
            # title = form.cleaned_data['title']
            
            location=request.GET.get('location')
            # location = form.cleaned_data['location']
            results=Job.objects.all()
            
            if tag != '0':
                tag=get_object_or_404(Tag,pk=tag)            
                results = results.filter(tag__name__icontains=tag.name).order_by('-created_date')
                
                if title:
                    results = Job.objects.annotate(search=SearchVector('title'),).filter(search=title,tag__name__icontains=tag.name).order_by('-created_date')
                if location:
                    results = Job.objects.annotate(search=SearchVector('county','location','address'),).filter(search=location,tag__name__icontains=tag.name).order_by('-created_date')
            else:
                if title:
                    results = Job.objects.annotate(search=SearchVector('title'),).filter(search=title).order_by('-created_date')
                if location:
                     results = Job.objects.annotate(search=SearchVector('county','location','address'),).filter(search=location).order_by('-created_date')
                
            # results = Job.objects.annotate(search=SearchVector('title','county','location','address','tag'),).filter(search=q).order_by('-created_date')
            page=request.GET.get('page',1)
            paginator = Paginator(results,30)
            try:
                results =paginator.page(page)
            except PageNotAnInteger:
                results=paginator.page(1)
            except EmptyPage:
                results=paginator.page(paginator.num_pages)
            
    return render(request,'pages/search.html',{'form':form,'results':results,'tag':tag,'title':title,'location':location })

def find(request):
    form = JobSearchForm
    results =[]
    
    # if form.is_valid('self'):
        # form = JobSearchForm(request.GET)
    if request.method =='GET':            
            q=request.GET.get('q')           
            results = Job.objects.annotate(search=SearchVector('title','county','location','address','tag'),).filter(search=q).order_by('-created_date')
            page=request.GET.get('page',1)
            paginator = Paginator(results,30)
            try:
                results =paginator.page(page)
            except PageNotAnInteger:
                results=paginator.page(1)
            except EmptyPage:
                results=paginator.page(paginator.num_pages)
            
    return render(request,'pages/search.html',{'form':form,'results':results,'q':q })


def error_404(request,exception):
    return render(request,'errors/4004.html')

def error_500(request):
    return render(request,'errors/500.html')
#      Channels
# stable
# Search docs
# Introduction
# Installation
# Tutorial
# Tutorial Part 1: Basic Setup
# Creating a project
# Creating the Chat app
# Add the index view
# Integrate the Channels library
# Tutorial Part 2: Implement a Chat Server
# Tutorial Part 3: Rewrite Chat Server as Asynchronous
# Tutorial Part 4: Automated Testing
# Consumers
# Routing
# Database Access
# Channel Layers
# Sessions
# Authentication
# Security
# Testing
# Worker and Background Tasks
# Deploying
# Troubleshooting
# ASGI
# Channel Layer Specification
# Community Projects
# Community Tutorials
# Contributing
# Support
# Release Notes
# Docs » Tutorial » Tutorial Part 1: Basic Setup Edit on GitHub
# Tutorial Part 1: Basic Setup
# Note

# If you encounter any issue during your coding session, please see the Troubleshooting section.

# In this tutorial we will build a simple chat server. It will have two pages:

# An index view that lets you type the name of a chat room to join.
# A room view that lets you see messages posted in a particular chat room.
# The room view will use a WebSocket to communicate with the Django server and listen for any messages that are posted.

# We assume that you are familiar with basic concepts for building a Django site. If not we recommend you complete the Django tutorial first and then come back to this tutorial.

# We assume that you have Django installed already. You can tell Django is installed and which version by running the following command in a shell prompt (indicated by the $ prefix):

# $ python3 -m django --version
# We also assume that you have Channels installed already. You can tell Channels is installed by running the following command:

# $ python3 -c 'import channels; print(channels.__version__)'
# This tutorial is written for Channels 3.0, which supports Python 3.6+ and Django 2.2+. If the Channels version does not match, you can refer to the tutorial for your version of Channels by using the version switcher at the bottom left corner of this page, or update Channels to the newest version.

# This tutorial also uses Docker to install and run Redis. We use Redis as the backing store for the channel layer, which is an optional component of the Channels library that we use in the tutorial. Install Docker from its official website - there are official runtimes for Mac OS and Windows that make it easy to use, and packages for many Linux distributions where it can run natively.

# Note

# While you can run the standard Django runserver without the need for Docker, the channels features we’ll be using in later parts of the tutorial will need Redis to run, and we recommend Docker as the easiest way to do this.

# Creating a project
# If you don’t already have a Django project, you will need to create one.

# From the command line, cd into a directory where you’d like to store your code, then run the following command:

# $ django-admin startproject mysite
# This will create a mysite directory in your current directory with the following contents:

# mysite/
#     manage.py
#     mysite/
#         __init__.py
#         asgi.py
#         settings.py
#         urls.py
#         wsgi.py
# Note

# Django 2.2 will not have the asgi.py file. Don’t worry, you can create it in a moment.

# Creating the Chat app
# We will put the code for the chat server in its own app.

# Make sure you’re in the same directory as manage.py and type this command:

# $ python3 manage.py startapp chat
# That’ll create a directory chat, which is laid out like this:

# chat/
#     __init__.py
#     admin.py
#     apps.py
#     migrations/
#         __init__.py
#     models.py
#     tests.py
#     views.py
# For the purposes of this tutorial, we will only be working with chat/views.py and chat/__init__.py. So remove all other files from the chat directory.

# After removing unnecessary files, the chat directory should look like:

# chat/
#     __init__.py
#     views.py
# We need to tell our project that the chat app is installed. Edit the mysite/settings.py file and add 'chat' to the INSTALLED_APPS setting. It’ll look like this:

# # mysite/settings.py
# INSTALLED_APPS = [
#     'chat',
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
# ]
# Add the index view
# We will now create the first view, an index view that lets you type the name of a chat room to join.

# Create a templates directory in your chat directory. Within the templates directory you have just created, create another directory called chat, and within that create a file called index.html to hold the template for the index view.

# Your chat directory should now look like:

# chat/
#     __init__.py
#     templates/
#         chat/
#             index.html
#     views.py
# Put the following code in chat/templates/chat/index.html:

# <!-- chat/templates/chat/index.html -->
# <!DOCTYPE html>
# <html>
# <head>
#     <meta charset="utf-8"/>
#     <title>Chat Rooms</title>
# </head>
# <body>
#     What chat room would you like to enter?<br>
#     <input id="room-name-input" type="text" size="100"><br>
#     <input id="room-name-submit" type="button" value="Enter">

#     <script>
#         document.querySelector('#room-name-input').focus();
#         document.querySelector('#room-name-input').onkeyup = function(e) {
#             if (e.keyCode === 13) {  // enter, return
#                 document.querySelector('#room-name-submit').click();
#             }
#         };

#         document.querySelector('#room-name-submit').onclick = function(e) {
#             var roomName = document.querySelector('#room-name-input').value;
#             window.location.pathname = '/chat/' + roomName + '/';
#         };
#     </script>
# </body>
# </html>
# Create the view function for the room view. Put the following code in chat/views.py:

# # chat/views.py
# from django.shortcuts import render

# def index(request):
#     return render(request, 'chat/index.html')
# To call the view, we need to map it to a URL - and for this we need a URLconf.

# To create a URLconf in the chat directory, create a file called urls.py. Your app directory should now look like:

# chat/
#     __init__.py
#     templates/
#         chat/
#             index.html
#     urls.py
#     views.py
# In the chat/urls.py file include the following code:

# # chat/urls.py
# from django.urls import path

# from . import views

# urlpatterns = [
#     path('', views.index, name='index'),
# ]
# The next step is to point the root URLconf at the chat.urls module. In mysite/urls.py, add an import for django.conf.urls.include and insert an include() in the urlpatterns list, so you have:

# # mysite/urls.py
# from django.conf.urls import include
# from django.urls import path
# from django.contrib import admin

# urlpatterns = [
#     path('chat/', include('chat.urls')),
#     path('admin/', admin.site.urls),
# ]
# Let’s verify that the index view works. Run the following command:

# $ python3 manage.py runserver
# You’ll see the following output on the command line:

# Watching for file changes with StatReloader
# Performing system checks...

# System check identified no issues (0 silenced).

# You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
# Run 'python manage.py migrate' to apply them.
# October 21, 2020 - 18:49:39
# Django version 3.1.2, using settings 'mysite.settings'
# Starting development server at http://127.0.0.1:8000/
# Quit the server with CONTROL-C.
# Go to http://127.0.0.1:8000/chat/ in your browser and you should see the text “What chat room would you like to enter?” along with a text input to provide a room name.

# Type in “lobby” as the room name and press enter. You should be redirected to the room view at http://127.0.0.1:8000/chat/lobby/ but we haven’t written the room view yet, so you’ll get a “Page not found” error page.

# Go to the terminal where you ran the runserver command and press Control-C to stop the server.

# Integrate the Channels library
# So far we’ve just created a regular Django app; we haven’t used the Channels library at all. Now it’s time to integrate Channels.

# Let’s start by creating a root routing configuration for Channels. A Channels routing configuration is an ASGI application that is similar to a Django URLconf, in that it tells Channels what code to run when an HTTP request is received by the Channels server.

# Start by adjusting the mysite/asgi.py file to include the following code:

# # mysite/asgi.py
# import os

# from channels.routing import ProtocolTypeRouter
# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     # Just HTTP for now. (We can add other protocols later.)
# })
# Note

# Django 2.2 doesn’t have inbuilt ASGI support so we need to use Channel’s fallback alternative. Create mysite/asgi.py like this:

# # mysite/asgi.py
# import os

# import django
# from channels.http import AsgiHandler
# from channels.routing import ProtocolTypeRouter

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
# django.setup()

# application = ProtocolTypeRouter({
#   "http": AsgiHandler(),
#   # Just HTTP for now. (We can add other protocols later.)
# })
# Now add the Channels library to the list of installed apps. Edit the mysite/settings.py file and add 'channels' to the INSTALLED_APPS setting. It’ll look like this:

# # mysite/settings.py
# INSTALLED_APPS = [
#     'channels',
#     'chat',
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
# ]
# You’ll also need to point Channels at the root routing configuration. Edit the mysite/settings.py file again and add the following to the bottom of it:

# # mysite/settings.py
# # Channels
# ASGI_APPLICATION = 'mysite.asgi.application'
# With Channels now in the installed apps, it will take control of the runserver command, replacing the standard Django development server with the Channels development server.

# Note

# The Channels development server will conflict with any other third-party apps that require an overloaded or replacement runserver command. An example of such a conflict is with whitenoise.runserver_nostatic from whitenoise. In order to solve such issues, try moving channels to the top of your INSTALLED_APPS or remove the offending app altogether.

# Let’s ensure that the Channels development server is working correctly. Run the following command:

# $ python3 manage.py runserver
# You’ll see the following output on the command line:

# Watching for file changes with StatReloader
# Performing system checks...

# System check identified no issues (0 silenced).

# You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
# Run 'python manage.py migrate' to apply them.
# October 21, 2020 - 19:08:48
# Django version 3.1.2, using settings 'mysite.settings'
# Starting ASGI/Channels version 3.0.0 development server at http://127.0.0.1:8000/
# Quit the server with CONTROL-C.
# Note

# Ignore the warning about unapplied database migrations. We won’t be using a database in this tutorial.

# Notice the line beginning with Starting ASGI/Channels version 3.0.0 development server at http://127.0.0.1:8000/. This indicates that the Channels development server has taken over from the Django development server.

# Go to http://127.0.0.1:8000/chat/ in your browser and you should still see the index page that we created before.

# Go to the terminal where you ran the runserver command and press Control-C to stop the server.

# This tutorial continues in Tutorial 2.

# © Copyright 2018, Django Software Foundation Revision 76fddba3.

# Built with Sphinx using a theme provided by Read the Docs.
#  Read the Docsv: stable 