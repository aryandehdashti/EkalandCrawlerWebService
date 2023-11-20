from django.urls import path

from .views import allProductsHistory, filterProductsByDate, lastCheckedProducts, filterProductsByIdentifier,filterProductsByProvider

urlpatterns = [
    path('all/', allProductsHistory, name='allHistory'),
    path('filteredByDate/', filterProductsByDate, name='filteredByDate'),
    path('filteredByIdentifier/', filterProductsByIdentifier, name='filterByIdentifier'),
    path('filteredByProvider/', filterProductsByProvider, name='filterByProvider'),
    path('', lastCheckedProducts),
]