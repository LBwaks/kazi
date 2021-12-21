from django import template
from ..models import Job
import datetime

register = template.Library()
@register.simple_tag
def recent_jobs():
    return Job.objects.filter(application_deadline__gte=datetime.datetime.now(),status='waiting').order_by('-created_date')[:5]