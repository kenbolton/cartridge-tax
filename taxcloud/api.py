
import suds

from django.conf import settings


class Client(object):
    """Client for TaxCloud's SOAP API"""
    url = "https://api.taxcloud.net/1.0/?wsdl"
    client = suds.client.Client(url)

    def lookup(self, request, **kwargs):
        #apiLoginID=None, apiKey=None,
            #cusomterID, cartID, cartItems, origin, destination,
            #deliveredBySeller, exemptCert):
        if apiLoginID is None:
            apiLoginID = settings.TAX_TAXCLOUD_API_ID
        if apiKey is None:
            apiKey = settings.TAX_TAXCLOUD_API_KEY
        customerID = request.user.id
        cartID = request.cart.id
        origin = settings.TAX_POSTCODE
        destination = request.order.shipping_detail_postcode
        deliveredBySeller = settings.TAX_DELIVER_BY_SELLER
        exemptCert = settings.TAX_EXEMPT_CERT

        return self.client.Lookup(apiLoginID, apiKey, cusomterID, CartID,
                CartItems, origin, destination, deliveredBySeller,
                exemptCert)
