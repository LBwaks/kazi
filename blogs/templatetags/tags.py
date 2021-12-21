from django import template
from blogs.models import Tag
from django.db.models import Count
register=template.Library()
@register.simple_tag
def get_all_tags():
    return Tag.objects.all().annotate(tag_count=Count('blog_tag'))