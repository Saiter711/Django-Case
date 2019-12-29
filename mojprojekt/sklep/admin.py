from django.contrib import admin
from .models import Product, Order, OrderedProduct, Complaint, Discount, Comment

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderedProduct)
admin.site.register(Complaint)
admin.site.register(Discount)
admin.site.register(Comment)

# Register your models here.
