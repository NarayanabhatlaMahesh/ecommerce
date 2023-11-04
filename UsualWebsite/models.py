from django.db import models

# Create your models here.
class SportsProduct(models.Model):
    name= models.CharField(max_length=100)
    cost=models.BigIntegerField()
    location=models.CharField(max_length=100)
    date=models.DateField()
    removedate=models.DateField()
    supplierName=models.CharField(max_length=100)
    image=models.CharField(max_length=200)
    description=models.TextField()

class userAuthenticate(models.Model):
    username= models.CharField(max_length=100,primary_key=True)
    password= models.CharField(max_length=100)
    location= models.CharField(max_length=100)
    phonenumber= models.CharField(max_length=12)

class userOrder(models.Model):
    location= models.CharField(max_length=100)
    ordersActive= models.CharField(max_length=100)
    count=models.BigIntegerField()
    username=models.ForeignKey(userAuthenticate, db_column='username' , on_delete=models.CASCADE)
    cost=models.BigIntegerField()