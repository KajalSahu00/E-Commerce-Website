from django.db import models
from django.conf import settings

gender = {('F', 'female'), ('M', 'male'), ('O', 'Other')}

class Customer(models.Model):
    mobile = models.CharField(max_length=10, null=False, blank=False, default="")
    isVerified = models.BooleanField(default=False)
    isCreated = models.BooleanField(default=False)

    def __str__(self):
        return self.mobile
    
class CustomerProfile(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    password = models.CharField(max_length=500)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    gender = models.CharField(max_length=1, choices=gender, default='F')

    def __str__(self):
        return self.name