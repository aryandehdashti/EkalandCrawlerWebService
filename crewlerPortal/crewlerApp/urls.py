from django.urls import path

from .views import allProductsHistory, lastCheckedProducts, filterProductsByCombo, logout_view, login_view, logs

urlpatterns = [
    path('accounts/login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('all/', allProductsHistory, name='allHistory'),
    # path('filteredByDate/', filterProductsByDate, name='filteredByDate'),
    # path('filteredByIdentifier/', filterProductsByIdentifier, name='filterByIdentifier'),
    # path('filteredByProvider/', filterProductsByProvider, name='filterByProvider'),
    path('filter/', filterProductsByCombo, name='comboFilter'),
    path('logs/', logs, name='comboFilter'),
    path('', lastCheckedProducts),

]