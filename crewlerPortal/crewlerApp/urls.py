from django.urls import path

from .views import allProductsHistory, filteredProducts, lastCheckedProducts

urlpatterns = [
    path('all/', allProductsHistory, name='allHistory'),
    path('filtered/', filteredProducts, name='filtered'),
    path('', lastCheckedProducts),
]