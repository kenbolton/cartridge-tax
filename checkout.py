import suds
from decimal import Decimal

from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import settings

from cartridge.shop.models import CartItem, Order, Product, ProductVariation
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
    settings.use_editable()
    if not request.session.get('free_shipping'):
        set_shipping(request, _("Flat rate shipping"),
                settings.SHOP_DEFAULT_SHIPPING_VALUE)


    if settings.TAX_SHIPPING:
        tax_shipping = \
                Decimal(str(request.session.get('shipping_total')))
    else:
        tax_shipping = Decimal(0)

    if not settings.TAX_SHIPPING_ADDRESS:
        tax_rate = Decimal(settings.TAX_FLAT_RATE) * Decimal(str(.01))
        total_tax = (request.cart.total_price() + tax_shipping) * \
                Decimal(tax_rate)
        set_salestax(request, _("Flat sales tax"),
                total_tax)
    else:
        api_key = settings.TAXCLOUD_API_KEY
        api_id = settings.TAXCLOUD_API_ID
        order = request.session.get('order')
        settings.use_editable()
        origin = (settings.TAX_SHOP_ADDRESS,
                settings.TAX_SHOP_ADDRESS2, settings.TAX_SHOP_CITY,
                settings.TAX_SHOP_STATE, settings.TAX_SHOP_POSTCODE,
                settings.TAX_SHOP_POSTCODE_PLUS4,)
        if len(str(order['shipping_detail_postcode']).replace('-','')) == 9:
            shipping_detail_postcode_plus4 = str(order['shipping_detail_postcode'])[:-4]
            shipping_detail_postcode = str(order['shipping_detail_postcode'])[0:4]
        else:
            shipping_detail_postcode = str(order['shipping_detail_postcode'])[0:4]
            shipping_detail_postcode_plus4 = '0000'

        destination = [
                order['shipping_detail_street'],
                '',
                order['shipping_detail_city'],
                shipping_detail_postcode,
                shipping_detail_postcode_plus4,
                ]
        cartItems = []
        items = CartItem.objects.filter(cart_id=request.session.get('cart'))
        for idx, item in enumerate(items):
            index = idx
            itemId = str(item.sku)
            productVariation = ProductVariation.objects.get(sku=itemId)
            product = Product.objects.get(id=productVariation.product_id)
            tic = str(product.tic)
            price = str(item.unit_price)
            quantity = item.quantity
            cartItem = (index, itemId, tic, price, quantity)
            cartItems.append(cartItem)
        shipping = (len(items) + 1, 'shipping', '11010',
                str(tax_shipping), 1)
        cartItems.append(shipping)
        url = "https://api.taxcloud.net/1.0/?wsdl"
        client = suds.client.Client(url)
        tax_total = client.service.Lookup(api_id, api_key,
                request.user.id, request.session.get('cart'),
                cartItems, origin, destination)
        set_salestax(request, tax_type, tax_total)
