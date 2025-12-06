from django_filters import FilterSet
from .models import Product


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'subcategory': ['exact'],
            'product_name': ['exact'],
            'price': ['gt', 'lt'],
            'article_number': ['exact'],

        }