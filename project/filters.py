import django_filters
from accounts.models import *
from charts.models import *


class ItemFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name='created', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='created', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='subcategory__category__name', lookup_expr='startswith')
    
    class Meta:
        model = Item
        fields = ['date_from', 'date_to','category']



class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='startswith')
    
    class Meta:
        model = ExpenseCategory
        fields = ['name']



class SubCategoryFilter(django_filters.FilterSet):
    category_name = django_filters.CharFilter(field_name='category__name', lookup_expr='startswith')
    name = django_filters.CharFilter(field_name='name', lookup_expr='startswith')
    
    class Meta:
        model = ExpenseSubCategory
        fields = ['name','category_name']



