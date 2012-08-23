from copy import deepcopy

from django.contrib import admin

from cartridge.shop.admin import ProductAdmin
from cartridge.shop.models import Product

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


admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)
