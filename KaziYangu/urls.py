"""KaziYangu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin, sitemaps
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404, url
from profiles.views import CustomPasswordChangeView
from django.contrib.sitemaps.views import sitemap
from jobs.sitemap import JobSitemap


sitemaps={
    'jobs': JobSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jobs/',include('jobs.urls')),
    path('applications/',include('applications.urls')),
    path("accounts/password/change/", CustomPasswordChangeView.as_view(), name="account_password_change"),
    path('accounts/', include('allauth.urls')),
    path('ratings/',include('star_ratings.urls',namespace="ratings")),
    path('profiles/', include('profiles.urls')),
    path('blogs/', include('blogs.urls')),
    path('', include('pages.urls')),
    
    path('sitemap.xml',sitemap,{'sitemaps':sitemaps},name='django.contrib.sitemaps.views.sitemap'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'pages.views.error_404'
handler500 = 'pages.views.error_500'
