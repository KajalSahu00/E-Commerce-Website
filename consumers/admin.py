from django.contrib import admin
from consumers.models import Customer, CustomerProfile

# Register your models here.
admin.site.register(Customer)
admin.site.register(CustomerProfile)