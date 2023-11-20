import datetime
from django.shortcuts import render
from django.http import  HttpResponseNotFound
from .models import Product
from itertools import groupby
import jdatetime
# Create your views here.

def convertPersianToGregorian(persian_date):
    year, month, day = persian_date.split('-')
    jalali_date = jdatetime.date(int(year), int(month), int(day))
    gregorian_date = jalali_date.togregorian()

    return f'{gregorian_date.year}-{gregorian_date.month}-{gregorian_date.day}'

def lastCheckedProducts(request):
    currentTime = datetime.datetime.now()
    try:
        lastFilterHours = currentTime - datetime.timedelta(hours=4)
        lastSeries = Product.objects.filter(dateTime__gte=lastFilterHours)
        hourFilter = request.POST.get("hours")
        if hourFilter is not None:
            try:
                hourFilter = int(hourFilter)
                lastFilterHours = currentTime - datetime.timedelta(hours=hourFilter)      
                lastSeries = Product.objects.filter(dateTime__gte=lastFilterHours)
                lastSeries = {k: list(v) for k, v in groupby(lastSeries, key=lambda x: x.identifier)}
                return render(request, 'lastChecked.html', {'lastSeries': lastSeries})
            except ValueError:
                pass
        else : return render(request, 'lastChecked.html', {'lastSeries': lastSeries})

    except Exception as e:
        return HttpResponseNotFound(f'Error: {e}')
        
def filterProductsByDate(request):
    try:
        filteredData = None
        fromDate = request.POST.get('fromDate')
        toDate = request.POST.get('toDate')
        if fromDate and toDate != None:
            # fromDate = convertPersianToGregorian(fromDate)
            # toDate = convertPersianToGregorian(toDate)

            filteredData = Product.objects.filter(dateTime__range=[fromDate, toDate]).order_by('identifier')

            filteredData = {k: list(v) for k, v in groupby(filteredData, key=lambda x: x.identifier)}

        return render(request, 'filteredByDate.html',{'filteredDataByDate':filteredData})
    except Exception as e:
        return HttpResponseNotFound(f'Error: {e}')
def filterProductsByIdentifier(request):
    try:
        identifier_ = request.POST.get('identifier')
        filteredData = Product.objects.filter(identifier=identifier_)
        return render(request, 'filteredByIdentifier.html', {'filteredProductsByIdentifier':filteredData})
    except Exception as e:
        return HttpResponseNotFound(f'Error: {e}')

def filterProductsByProvider(request):
    try:
        provider_ = request.POST.get('provider')
        filteredData = Product.objects.filter(supplier=provider_).order_by('identifier')

        filteredData = {k: list(v) for k, v in groupby(filteredData, key=lambda x: x.identifier)}

        return render(request, 'filteredByProvider.html', {'filteredProductsByProvider':filteredData})
    except Exception as e:
        return HttpResponseNotFound(f'Error: {e}')

def allProductsHistory(request):
    try:
        allData = Product.objects.all()
        allData = {k: list(v) for k, v in groupby(allData, key=lambda x: x.identifier)}

        return render(request, 'allHistory.html',{'allData':allData})
    except Exception as e:
        return HttpResponseNotFound(f'Error: {e}')