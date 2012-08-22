
import suds

from django.conf import settings


class TaxcloudClient(object):
    """Client for TaxCloud's SOAP API"""
    url = "https://api.taxcloud.net/1.0/?wsdl"
    client = suds.client.Client(url)
    api_key = settings.TAXCLOUD_API_KEY
    api_id = settings.TAXCLOUD_API_ID

    def lookup(self, apiLoginID=self.api_id, apiKey=self.api_key,
            cusomterID, cartID, cartItems, origin, destination,
            deliveredBySeller, exemptCert):
        return self.client.Lookup(apiLoginID, apiKey, cusomterID, CartID,
                CartItems, origin, destination, deliveredBySeller,
                exemptCert)
