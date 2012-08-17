from copy import deepcopy

from django.contrib import admin

from cartridge.shop.admin import ProductAdmin
from cartridge.shop.models import Product

product_fieldsets = deepcopy(ProductAdmin.fieldsets)
product_fieldsets[0][1]["fields"].insert(2, "taxable")


class ProductAdmin(ProductAdmin):
    fieldsets = product_fieldsets

admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)
