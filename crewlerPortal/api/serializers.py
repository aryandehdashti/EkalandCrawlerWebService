from rest_framework import serializers
from crewlerApp.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'color', 'status', 'warranty', 'price', 'insurance', 'supplier', 'url', 'dateTime')