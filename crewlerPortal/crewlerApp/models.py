from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    warranty = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    insurance = models.CharField(max_length=100, default='ندارد')
    supplier = models.CharField(max_length=20)
    url = models.CharField(max_length=250)
    dateTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title+ ' '+self.dateTime.strftime("%m/%d - %H:%M")

