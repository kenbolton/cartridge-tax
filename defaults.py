from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import register_setting

#taxable = (
    #"cartridge.shop.models.Product.taxable",
    #"BooleanField",
    #("Taxable",),
    #{"default": True, },
    #)
#emf = list(settings.EXTRA_MODEL_FIELDS)
#emf.append(taxable)
#settings.EXTRA_MODEL_FIELDS = tuple(emf)

    
register_setting(
    name="TAX_FLAT_RATE",
    label=_("Tax Flat Rate"),
    description=_("Flat tax rate to charge if we are not taxing to shipping address."),
    editable=True,
    default="8.875",
)

register_setting(
    name="TAX_SHIPPING_ADDRESS",
    label=_("Tax Shipping Address"),
    description=_("Charge tax to the shipping address."),
    editable=True,
    default=True,
)

register_setting(
    name="TAX_TAXCLOUD_API_KEY",
    label=_("TaxCloud API Key"),
    description=_("Key for the TaxCloud API"),
    editable=True,
    default="",
)

register_setting(
    name="TAX_DISCOUNT_CATEGORIES",
    label=_("Tax Discount Categories"),
    description=_("Categories that will be taxed at a discounted rate."),
    editable=True,
    default="",
)

register_setting(
    name="TAX_DISCOUNT_RATE",
    label=_("Tax Discount Rate"),
    description=_("Rate that will be taxed for discounted items."),
    editable=True,
    default="",
)


