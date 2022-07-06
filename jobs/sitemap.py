from django.contrib.sitemaps import Sitemap
from .models import Job

class JobSitemap(Sitemap):
    changefreq ='weekly'
    priority= 0.5

    def items(self):
        return Job.objects.all()

    def lastmod(self,obj):
        return obj.created_date
            
    