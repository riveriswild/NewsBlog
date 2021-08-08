import django_filters
from django_filters import FilterSet
from news.models import Post
from django.forms import DateInput, Select, CheckboxInput

class PostFilter(FilterSet):
    date = django_filters.DateFilter(field_name='dateCreation', widget=DateInput(attrs={'type': 'date'}),
                                     lookup_expr='gt',
                                     label='Позже, чем')
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author': ['exact'],
            'postCategory': ['exact'],
        }