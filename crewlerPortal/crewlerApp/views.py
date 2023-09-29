import datetime
from django.shortcuts import render
from django.http import  HttpResponseNotFound
from .models import Product
# Create your views here.

def lastCheckedProducts(request):
    try:
        currentTime = datetime.datetime.now()
        last12hours = currentTime - datetime.timedelta(hours=12)       
        lastSeries = Product.objects.filter(dateTime__gte=last12hours)
        return render(request, 'lastChecked.html', {'lastSeries': lastSeries})
    except Exception as e:
        return HttpResponseNotFound(f'Error: {e}')
    
def filteredProducts(request):
    try:
        fromDate = request.POST.get('fromDate')
        toDate = request.POST.get('toDate')
        filteredData = Product.objects.filter(dateTime__range=[fromDate, toDate])
        return render(request, 'filtered.html',{'filteredData':filteredData})
    except Exception as e:
        return HttpResponseNotFound(f'Error: {e}')

def allProductsHistory(request):
    try:
        allData = Product.objects.all()
        return render(request, 'allHistory.html',{'allData':allData})
    except Exception as e:
        return HttpResponseNotFound(f'Error: {e}')