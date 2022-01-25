from django.contrib import admin

from shop.models import Section, Product, Discount, Order, OrderLine

admin.site.register(Section)
admin.site.register(Product)
admin.site.register(Discount)
admin.site.register(Order)
admin.site.register(OrderLine)

