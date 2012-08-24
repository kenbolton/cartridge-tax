from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import register_setting


register_setting(
        name="TAX_STREET_ADDRESS",
        label=_("Shop's Street Address."),
        description=_("Street address of the originating shipping \
            address."),
        editable=True,
        default="",
        )

register_setting(
        name="TAX_STREET_ADDRESS2",
        label=_("Shop's Street Address, Second Line"),
        description=_("Street address of the originating shipping \
            address."),
        editable=True,
        default="",
        )

register_setting(
        name="TAX_CITY",
        label=_("Shop's City"),
        description=_("City of the originating shipping address."),
        editable=True,
        default="",
        )

register_setting(
        name="TAX_STATE",
        label=_("Shop's State"),
        description=_("State of the originating shipping address."),
        editable=True,
        default="",
        )

register_setting(
        name="TAX_POSTCODE",
        label=_("Shop's Postcode"),
        description=_("Postcode of the originating shipping address."),
        editable=True,
        default="",
        )

register_setting(
        name="TAX_POSTCODE_PLUS4",
        label=_("Shop's Postcode Plus 4"),
        description=_("Postcode-plus-4 of the originating shipping address."),
        editable=True,
        default="",
        )

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
