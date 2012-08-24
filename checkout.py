from decimal import Decimal

from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import settings

from cartridge.shop.models import Order
from cartridge.shop.utils import set_shipping

from utils import set_salestax

from taxcloudapi import TaxCloudClient

def tax_billship_handler(request, order_form):
    """
    Tax/billing/shipping handler - called when the first step in
    the checkout process with billing/shipping address fields is
    submitted. Implement your own and specify the path to import it
    from via the setting ``SHOP_HANDLER_BILLING_SHIPPING``.
    This function will typically contain any shipping calculation
    where the shipping amount can then be set using the function
    ``cartridge.shop.utils.set_shipping``. The Cart object is also
    accessible via ``request.cart``
    """
    if not request.session.get('free_shipping'):
        settings.use_editable()
        set_shipping(request, _("Flat rate shipping"),
                     settings.SHOP_DEFAULT_SHIPPING_VALUE)

    if settings.TAX_SHIPPING:
        tax_shipping = \
                Decimal(str(request.session.get('shipping_total')))
    else:
        tax_shipping = Decimal(0)

    if not request.session.get('tax_shipping_address'):
        settings.use_editable()
        tax_rate = Decimal(settings.TAX_FLAT_RATE) * Decimal(str(.01))
        set_salestax(request, _("Flat sales tax"),
                    (request.cart.total_price() + tax_shipping) *
                    Decimal(tax_rate))
    else:
        api_key = settings.TAXCLOUD_API_KEY
        api_id = settings.TAXCLOUD_API_ID
        order = request.order
        settings.use_editable()
        origin = (settings.TAX_SHOP_ADDRESS,
                settings.TAX_SHOP_ADDRESS2, setttings.TAX_SHOP_CITY,
                settings.TAX_SHOP_STATE, settings.TAX_SHOP_POSTCODE,
                settings.TAX_SHOP_POSTCODE_PLUS4,)
        if order.shipping_detail_postcode.replace('-','').length == 9:
            shipping_detail_postcode_plus4 = order.shipping_detail_postcode[:-4]
            shipping_detail_postcode = order.shipping_detail_postcode[0:4]
        else:
            shipping_detail_postcode = order.shipping_detail_postcode[0:4]
            shipping_detail_postcode_plus4 = '0000'

        destination = [
                order.shipping_detail_street,
                order.shipping_detail_street2,
                order.shipping_detail_city,
                shipping_detail_postcode,
                shipping_detail_postcode_plus4,
                ]
        cartItems = []
        for item in request.cart.items:
            print dir(item)
        print TaxCloudClient.lookup(api_id, api_key,
                request.user.id, request.cart.id, cartItems,
                origin, destination)
