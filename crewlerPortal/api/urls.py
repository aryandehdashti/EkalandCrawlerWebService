from django.urls import path
from .views import *

urlpatterns = [
    path('all/',GetAllProductHistory.as_view()),
    path('', GetLastSeriesProducts.as_view()),
    path('filter/', GetFilteredProducts.as_view())
]
