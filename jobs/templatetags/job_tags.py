from django import template
from jobs.models import Tag 
from django.db.models import Count
register = template.Library()
@register.simple_tag
def get_tags():
    return Tag.objects.all().annotate(tags_count=Count('job'))
    #  return Job.objects.filter(tag_slug=self.tag_slug).exclude(slug=self.slug)

    