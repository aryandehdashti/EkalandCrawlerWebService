from django.db import models

# Create your models here.
# class sourceProduct(models.Model):
#     identifier = models.CharField(max_length=200, null=False, blank=False, unique=True)
#     title = models.CharField(max_length=100, null=False, blank=False, unique=True)
#     digikalaURL = models.URLField(null=True,blank=True, unique=True)
#     baninopcURL = models.URLField(null=True,blank=True, unique=True)
#     berozkalaURL = models.URLField(null=True,blank=True, unique=True)
#     exoURL = models.URLField(null=True,blank=True, unique=True)
#     lioncomputerURL = models.URLField(null=True,blank=True, unique=True)
#     meghdaditURL = models.URLField(null=True,blank=True, unique=True)
#     shopmitURL = models.URLField(null=True,blank=True, unique=True)
#     toprayanURL= models.URLField(null=True, blank=True, unique=True)
#     is_active = models.BooleanField(default=True)

class SourceProduct(models.Model):
    identifier = models.CharField(max_length=200, null=False, blank=False, unique=False)
    title = models.CharField(max_length=100, null=False, blank=False, unique=False)
    URL = models.URLField(null=True,blank=True, unique=False)
    provider = models.CharField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.identifier+ ' '+self.title+ ' '+ self.provider

class Product(models.Model):
    identifier = models.CharField(max_length=255)
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

