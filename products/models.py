from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, default='Female Dresses')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50, default='Sera')
    price = models.IntegerField(default=1000)
    description = models.CharField(max_length=100, default='')
    image = models.ImageField(upload_to='media/')
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name