from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import register_setting


register_setting(
        name="TAX_SHOP_ADDRESS",
        label=_("Shop Street Address"),
        description=_("Street address of the originating shipping \
            address."),
        editable=True,
        default="",
        )

register_setting(
        name="TAX_SHOP_ADDRESS2",
        label=_("Shop Street Address, Second Line"),
        description=_("Street address of the originating shipping \
            address."),
        editable=True,
        default="",
        )

register_setting(
        name="TAX_SHOP_CITY",
        label=_("Shop City"),
        description=_("City of the originating shipping address."),
        editable=True,
        default="",
        )

register_setting(
        name="TAX_SHOP_STATE",
        label=_("Shop State"),
        description=_("State of the originating shipping address."),
        editable=True,
        default="",
        )

register_setting(
        name="TAX_SHOP_POSTCODE",
        label=_("Shop Postcode"),
        description=_("Postcode of the originating shipping address."),
        editable=True,
        default="",
        )

register_setting(
        name="TAX_SHOP_POSTCODE_PLUS4",
        label=_("Shop Postcode Plus 4"),
        description=_("Postcode-plus-4 of the originating shipping address."),
        editable=True,
        default="",
        )

register_setting(
        name="TAX_OUT_OF_STATE",
        label=_("Tax Out Of State"),
        description=_("Apply flat rate tax to shipping addresses \
                outside of shop's state."),
        editable=True,
        default=False,
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
        default=False,
        )

register_setting(
        name="TAX_SHIPPING",
        label=_("Tax Shipping Cost"),
        description=_("Apply sales tax to the cost of shipping"),
        editable=True,
        default=True,
        )

register_setting(
        name="TAX_USE_TAXCLOUD",
        label=_("Use TaxCloud.net API"),
        # XXX Change description when this feature works.
        description=_("Enable use of the TaxCloud.net API. USA \
                merchants only. (<em>Experimental</em>)"),
        editable=True,
        default=False,
        )

register_setting(
        name="TAX_TAXCLOUD_API_ID",
        label=_("TaxCloud API ID"),
        description=_("ID for the TaxCloud API"),
        editable=True,
        default="",
        )

register_setting(
        name="TAX_TAXCLOUD_API_KEY",
        label=_("TaxCloud API Key"),
        description=_("Key for the TaxCloud API"),
        editable=True,
        default="",
        )
