from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=100,null=True,blank=True)
    color = models.CharField(max_length=50,null=True,blank=True)
    status = models.CharField(max_length=50,null=True,blank=True)
    warranty = models.CharField(max_length=100,null=True,blank=True)
    price = models.CharField(max_length=50,null=True,blank=True)
    insurance = models.CharField(max_length=100, default='ندارد',null=True,blank=True)
    supplier = models.CharField(max_length=20,null=True,blank=True)
    url = models.CharField(max_length=250,null=True,blank=True)
    dateTime = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self):
        return self.title+ ' '+self.dateTime.strftime("%m/%d - %H:%M")

