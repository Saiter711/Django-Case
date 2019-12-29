from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Product(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)
    price = models.FloatField(default =0)
    desc = models.CharField(max_length=500)
    producent = models.CharField(max_length=40)
    rok = models.IntegerField(default =0)


class Comment(models.Model):
    grade = models.IntegerField(default=0, validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ])
    comment = models.CharField(max_length=300)
    nickname = models.CharField(max_length=50, default = "Anonim")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)


class Discount(models.Model):

    def __str__(self):
        return str(self.name)

    name = models.CharField(max_length=50)
    discount = models.IntegerField(default=0)


class Order(models.Model):

    def __str__(self):
        return str(self.first_name) + " " + str(self.surname)

    def get_total_price(self):
        total = 0
        ordered_products = OrderedProduct.objects.filter(order = self)
        for ordered_product in ordered_products:
            total += ordered_product.amount *ordered_product.product.price
        return total

    def get_ordered_products(self):
        ordered_products = OrderedProduct.objects.filter(order=self)
        return ordered_products

    ordered_products = models.ManyToManyField("Product", through ="OrderedProduct")
    discount_code = models.ForeignKey(Discount, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    send = models.CharField(max_length=100)


class OrderedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete= models.CASCADE)
    amount = models.IntegerField(default = 1)


class Complaint(models.Model):
    def __str__(self):
        return str(self.name)
    name = models.CharField(max_length=50)
    message = models.CharField(max_length=500)



