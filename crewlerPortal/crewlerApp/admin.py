from django.contrib import admin
from .models import Product,SourceProduct

# Register your models here.
admin.site.register(Product)
admin.site.register(SourceProduct)