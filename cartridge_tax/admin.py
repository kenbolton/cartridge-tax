from copy import deepcopy

from django.contrib import admin
from django.db.models import DecimalField

from cartridge.shop.admin import ProductAdmin, OrderAdmin
from cartridge.shop.forms import MoneyWidget
from cartridge.shop.fields import MoneyField
from cartridge.shop.models import Product, Order

product_fieldsets = deepcopy(ProductAdmin.fieldsets)
product_fieldsets[0][1]["fields"].insert(2, "tic")
product_media_css = deepcopy(ProductAdmin.Media.css)
product_media_js = deepcopy(ProductAdmin.Media.js)
product_media_js = product_media_js + ("js/taxcloud-tic.js",)


class ProductAdmin(ProductAdmin):
    fieldsets = product_fieldsets

    class Media:
        css = product_media_css
        js = product_media_js

order_fieldsets = deepcopy(OrderAdmin.fieldsets)
order_fieldsets[2][1]["fields"] = list(order_fieldsets[2][1]["fields"])
order_fieldsets[2][1]["fields"].insert(4, ('tax_total', 'tax_type'))

class OrderAdmin(OrderAdmin):
    fieldsets = order_fieldsets
    formfield_overrides = {MoneyField: {"widget": MoneyWidget}, DecimalField: {"widget": MoneyWidget}}

admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)
admin.site.unregister(Order)
admin.site.register(Order, OrderAdmin)
