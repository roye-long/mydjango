

from django.db import models

# Create your models here.


class Jd(models.Model):
    price=models.CharField(max_length=20)
    color=models.CharField(max_length=20)
    productID=models.CharField(max_length=20)
    time=models.CharField(max_length=20)
    shop=models.CharField(max_length=20)
    shop_url=models.CharField(max_length=50)
    weight=models.CharField(max_length=20)
    addr=models.CharField(max_length=20)
    material=models.CharField(max_length=50)
    popEle=models.CharField(max_length=20)
    marketTime=models.CharField(max_length=20)
    sleeves_type=models.CharField(max_length=20)
    style=models.CharField(max_length=20)
    version_type=models.CharField(max_length=20)
    thickness=models.CharField(max_length=20)
    length=models.CharField(max_length=20)
    yimenjin=models.CharField(max_length=20)
    collar=models.CharField(max_length=20)
    pattern=models.CharField(max_length=20)
    elseInfo=models.CharField(max_length=250)
    title=models.CharField(max_length=20)
    category=models.CharField(max_length=20)
    url=models.CharField(max_length=50)
    size=models.CharField(max_length=20)
    image_urls=models.CharField(max_length=50)
    images=models.CharField(max_length=50)
class Newline(models.Model):
    xinqi=models.CharField(max_length=10)
    maxs=models.IntegerField(default=0)
    minx =models.IntegerField(default=0)