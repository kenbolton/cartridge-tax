import suds

from decimal import Decimal

from time import time

from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import settings

from cartridge.shop.models import CartItem, Order, Product, ProductVariation
from cartridge.shop.utils import set_shipping
from cartridge.shop.checkout import CheckoutError

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

    if request.session.get('tax_total'):
        del request.session['tax_total']

    if not settings.TAX_USE_TAXCLOUD:
        if settings.TAX_OUT_OF_STATE or \
                request.session.get('order')['shipping_detail_state'] \
                    == settings.TAX_SHOP_STATE:
            # Use the flat rate
            tax_rate = Decimal(settings.TAX_FLAT_RATE) * Decimal(str(.01))
            tax_total = (request.cart.total_price() + tax_shipping) * \
                Decimal(tax_rate)
            set_salestax(request, _("Flat sales tax"), tax_total)
        else:
            # Sweet: no sales tax
            set_salestax(request, _("Out of state"), Decimal(0))
    else:  # Use TaxCloud.net SOAP service.
        #request.session['tax_total'] = 0
        api_key = settings.TAX_TAXCLOUD_API_KEY
        api_id = settings.TAX_TAXCLOUD_API_ID
        url = "https://api.taxcloud.net/1.0/?wsdl"
        client = suds.client.Client(url)
        order = request.session.get('order')
        settings.use_editable()
        origin = client.factory.create('Address')
        origin.Address1 = settings.TAX_SHOP_ADDRESS
        origin.Address2 = settings.TAX_SHOP_ADDRESS2
        origin.City = settings.TAX_SHOP_CITY
        origin.State = settings.TAX_SHOP_STATE
        origin.Zip5 = settings.TAX_SHOP_POSTCODE
        origin.Zip4 = settings.TAX_SHOP_POSTCODE_PLUS4
        if len(str(order['shipping_detail_postcode']).replace('-','')) == 9:
            shipping_detail_postcode_plus4 = \
                    str(order['shipping_detail_postcode'])[:-4]
            shipping_detail_postcode = \
                    str(order['shipping_detail_postcode'])[0:5]
        else:
            shipping_detail_postcode = \
                    str(order['shipping_detail_postcode'])[0:5]
            shipping_detail_postcode_plus4 = '0000'
        destination = client.factory.create('Address')
        destination.Address1 = order['shipping_detail_street']
        destination.Address2 = ''
        destination.City = order['shipping_detail_city']
        destination.State = order['shipping_detail_state']
        destination.Zip5 = shipping_detail_postcode
        destination.Zip4 = shipping_detail_postcode_plus4
        ArrayOfCartItem = client.factory.create('ArrayOfCartItem')
        items = CartItem.objects.filter(cart_id=request.session.get('cart'))
        for idx, item in enumerate(items):
            cartItem = client.factory.create('CartItem')
            cartItem.Index = idx + 1
            cartItem.ItemID = str(item.sku)
            productVariation = ProductVariation.objects.get(sku=item.sku)
            product = Product.objects.get(id=productVariation.product_id)
            cartItem.TIC = int(product.tic)
            cartItem.Price = float(item.unit_price)
            cartItem.Qty = float(item.quantity)
            ArrayOfCartItem.CartItem.append(cartItem)
        shipping = client.factory.create('CartItem')
        shipping.Index = len(items) + 1
        shipping.ItemID = str('shipping')
        shipping.TIC = int(11010)
        shipping.Price = float(tax_shipping)
        shipping.Qty = float(1)
        ArrayOfCartItem.CartItem.append(shipping)
        cartID = str(request.COOKIES.get('sessionid')) +'-' + str(time())
        request.session['cartID'] = cartID
        request.session.modified = True
        try:
            result = client.service.Lookup(str(api_id), str(api_key),
                str(request.user.id),
                cartID,
                ArrayOfCartItem, origin, destination, False
                )
            tax_total = 0
        except:
            raise CheckoutError("Unable to contact the TaxCloud \
            server.")
        if str(result.ResponseType) == 'OK' and \
                result.CartID == cartID:
            for CartItemResponse in result.CartItemsResponse[0]:
                tax_total += CartItemResponse.TaxAmount
        else:
            raise CheckoutError(result.Messages)
        print tax_total
        set_salestax(request, _("Sales tax for shipping address"), tax_total)


def tax_order_handler(request, order_form, order):
    """
    Default order handler - called when the order is complete and
    contains its final data. Implement your own and specify the path
    to import it from via the setting ``SHOP_HANDLER_ORDER``.
    """
    order.tax_total = Decimal(str(request.session.get('tax_total')))
    order.total += order.tax_total
    if settings.TAX_USE_TAXCLOUD_AUTHORIZATION:
        api_key = settings.TAX_TAXCLOUD_API_KEY
        api_id = settings.TAX_TAXCLOUD_API_ID
        url = "https://api.taxcloud.net/1.0/?wsdl"
        client = suds.client.Client(url)
        result = client.service.Authorized(
                    str(api_id),  # xs:string apiLoginID,
                    str(api_key),  # xs:string apiKey
                    str(request.user.id),  # xs:string customerID
                    request.session['cartID'],  # xs:string cartID
                    str(order.id),  # xs:string orderID
                    order.time,  # xs:dateTime dateAuthorized
                    )
        if str(result.ResponseType) == 'OK':
            captured = client.service.Captured(str(api_id), str(api_key),
                    str(order.id))
            if str(captured.ResponseType) == 'OK':
                pass
            else:
                raise CheckoutError(result.Messages)
        else:
            raise CheckoutError(result.Messages)
    order.save()
    del request.session['tax_type']
    del request.session['tax_total']
    del request.session['cartID']


