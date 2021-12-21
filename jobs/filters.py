from autoslug import fields
import django_filters
from django_filters.filters import ChoiceFilter
from .models import Job



class MyJobFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model= Job
        fields = ['tag','location']
        