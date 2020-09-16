from django.db import models
from django.contrib.auth.models import User

class SalesPerson(models.Model):
    GENDER = [
        ('M','Male'),
        ('F','Female'),
    ]
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    gender = models.CharField(choices=GENDER, max_length=9)
    nrc = models.CharField(max_length=20)
    phone = models.CharField(max_length=30)
    location = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username}"


class Category(models.Model):

    category_id = models.AutoField(primary_key=True, auto_created=True)
    category_name = models.CharField(max_length=50, unique=True, )

    def __str__(self):
        return f"{self.category_name}"


class Stock(models.Model):
    category = models.ForeignKey('Category',
                                 on_delete=models.CASCADE)
    product_id = models.CharField(primary_key=True, max_length=50)
    product_name = models.CharField(max_length=100, unique=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    create_dated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_name}"


class Sale(models.Model):
    user = models.ForeignKey(SalesPerson,
                                on_delete=models.CASCADE, blank=True)

    product = models.ForeignKey('Stock',
                                on_delete=models.CASCADE)

    category = models.ForeignKey('Category',
                                 on_delete=models.CASCADE)

    quantity = models.IntegerField(null=False)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2,default=0.00,null=True,blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.product_name}"


class Refund(models.Model):
    user = models.ForeignKey(SalesPerson,
                                on_delete=models.CASCADE, blank=True)

    product = models.ForeignKey(Stock,
                                on_delete=models.CASCADE)

    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE)

    quantity = models.IntegerField(null=False)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    reason_for_refund = models.TextField(max_length=400)

    def __str__(self):
        return f"{self.reason_for_refund}"

