import datetime
from rest_framework import generics, views
from crewlerApp.models import Product
from .serializers import ProductSerializer

class GetAllProductHistory(generics.ListAPIView):
    try:
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
    except:pass

class GetLastSeriesProducts(generics.ListAPIView):
    try:
        currentTime = datetime.datetime.now()
        last12hours = currentTime - datetime.timedelta(hours=12)       
        queryset = Product.objects.filter(dateTime__gte=last12hours)
        serializer_class = ProductSerializer
    except: pass

class GetFilteredProducts(views.APIView):
    try:
        def post(self, request):
            fromDate = request.data.get('fromDate')
            toDate = request.data.get('toDate')
            if toDate is None and fromDate is None:
                return views.Response({'error':'wrong Input'}, status=400)

            filteredData = Product.objects.filter(dateTime__range=[fromDate, toDate])
            serializer = ProductSerializer(filteredData)
            if serializer.is_valid():
                return views.Response(serializer.data, status=200)
            return views.Response(serializer.errors, status=400)
    except: pass

