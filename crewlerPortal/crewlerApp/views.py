import datetime
from django.shortcuts import render
from django.http import  HttpResponse, HttpResponseNotFound
import openpyxl
import pytz
from .models import Product
from itertools import groupby
import jdatetime
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(lastCheckedProducts)  
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect(login_view)

def convertPersianToGregorian(persian_date):
    year, month, day = persian_date.split('-')
    jalali_date = jdatetime.date(int(year), int(month), int(day))
    gregorian_date = jalali_date.togregorian()

    return f'{gregorian_date.year}-{gregorian_date.month}-{gregorian_date.day}'

@login_required
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
                lastSeries = {k: [product for product in lastSeries if product.identifier == k] for k in set([p.identifier for p in lastSeries])}
                return render(request, 'lastChecked.html', {'lastSeries': lastSeries})
            except ValueError:
                pass
        else : return render(request, 'lastChecked.html', {'lastSeries': lastSeries})

    except Exception as e:
        return HttpResponseNotFound(f'Error: {e}')

@login_required      
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
# def filterProductsByIdentifier(request):
#     try:
#         identifier_ = request.POST.get('identifier')
#         filteredData = Product.objects.filter(identifier=identifier_)
#         return render(request, 'filteredByIdentifier.html', {'filteredProductsByIdentifier':filteredData})
#     except Exception as e:
#         return HttpResponseNotFound(f'Error: {e}')

# def filterProductsByProvider(request):
#     try:
#         provider_ = request.POST.get('provider')
#         filteredData = Product.objects.filter(supplier=provider_).order_by('identifier')

#         filteredData = {k: list(v) for k, v in groupby(filteredData, key=lambda x: x.identifier)}

#         return render(request, 'filteredByProvider.html', {'filteredProductsByProvider':filteredData})
#     except Exception as e:
#         return HttpResponseNotFound(f'Error: {e}')

@login_required
def allProductsHistory(request):
    try:
        allProducts = Product.objects.all()
        allData = {k: [product for product in allProducts if product.identifier == k] for k in set([p.identifier for p in allProducts])}
        return render(request, 'allHistory.html',{'allData':allData})
    except Exception as e:
        return HttpResponseNotFound(f'Error: {e}')
    
@login_required
def filterProductsByCombo(request):
    try:
        filteredData = None
        form_data = {  # Store form data for persistence
            'fromDate': request.POST.get('fromDate', ''),
            'toDate': request.POST.get('toDate', ''),
            'identifier': request.POST.get('identifier', ''),
            'provider': request.POST.get('provider', ''),
        }
        products = Product.objects.all()

        if form_data['fromDate'] and form_data['toDate']:
            from_datetime = datetime.datetime.strptime(form_data['fromDate'], '%Y-%m-%d')  
            to_datetime = datetime.datetime.strptime(form_data['toDate'], '%Y-%m-%d')  
            to_datetime = to_datetime.replace(hour=23, minute=59, second=59, microsecond=999999)
            products = products.filter(dateTime__range=[from_datetime, to_datetime])
        if form_data['identifier']:
            products = products.filter(identifier=form_data['identifier'])
        if form_data['provider']:
            products = products.filter(supplier__icontains=form_data['provider'])        
        filteredData = {k: [product for product in products if product.identifier == k] for k in set([p.identifier for p in products])}

        filename = datetime.datetime.now().strftime('%c')
        
        if request.method == 'POST' and 'download_excel' in request.POST:
            workbook = openpyxl.Workbook()
            worksheet = workbook.active

            headers = ['Identifier', 'title', 'supplier','color', 'price','status','waranty','Insurance','DateTime', 'url' ]
            worksheet.append(headers)

            for identifier, products in filteredData.items():
                for product in products:
                    row = [product.identifier, product.title, product.supplier, product.color, product.price, product.status, product.warranty, product.insurance, product.dateTime.astimezone(pytz.timezone('Asia/Tehran')).replace(tzinfo=None), product.url]  
                    worksheet.append(row)

            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
            workbook.save(response)
            return response
        return render(request, 'comboFilter.html', {'filteredData': filteredData, 'form_data': form_data})

    except Exception as e:
        return HttpResponseNotFound(f'Error: {e}')
    

@login_required
def logs(request):
    try:
        with open('product_parser.log', "r") as log_file:
            log_data = log_file.readlines()
    except FileNotFoundError:
        log_data = ["Log file not found"]
    context = {"log_data": log_data}
    return render(request, "logs.html", context)