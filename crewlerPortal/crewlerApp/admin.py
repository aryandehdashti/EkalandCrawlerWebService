from django.contrib import admin
from .models import Product,SourceProduct


@admin.action(description='Activate selected products')
def activate_products(self, request, queryset):
    queryset.update(is_active=True)

@admin.action(description='Deactivate selected products')
def deactivate_products(self, request, queryset):
    queryset.update(is_active=False)

class SourceProductAdmin(admin.ModelAdmin):
    list_display = ['identifier', 'title', 'provider', 'is_active']
    actions = [activate_products,deactivate_products]
    search_fields = ['identifier', 'title', 'provider']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['identifier', 'title', 'supplier', 'color', 'dateTime','status']
    search_fields = ['identifier', 'title', 'supplier', 'color']



admin.site.register(Product,ProductAdmin)
admin.site.register(SourceProduct, SourceProductAdmin)# Register your models here.
