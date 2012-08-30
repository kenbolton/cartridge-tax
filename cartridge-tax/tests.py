from decimal import Decimal

from django.test import TestCase

from cartridge.shop.models import Cart
from cartridge.shop.tests import ShopTests

from cartridgetax.handler import default_billship_handler

class MockRequest(object):
    pass


class TaxTests(ShopTests):

#class TaxTests(TestCase):

    def setUp(self):
        """
        Set up test data - Not sure what needs to be setup yet.
        """
        return super(TaxTests, self).setUp()

    def test_default_billshipping(self):
        self._reset_variations()
        variation = self._product.variations.all()[0]
        self._add_to_cart(variation, 1)
        cart = Cart.objects.from_request(self.client)

        request = MockRequest()
        request.cart = cart
        order_form = ""

        #request.session = {'tax_shipping_address': True}
        #result = default_billship_handler(request, order_form)
        #self.assertEqual(request.session['tax_type'], 'Flat sales tax')
        #self.assertEqual(request.session['tax_total'], Decimal('177.500'))

        request.session = {'tax_shipping_address': False}
        result = default_billship_handler(request, order_form)
        self.assertEqual(request.session['tax_type'], 'Flat sales tax')
        self.assertEqual(request.session['tax_total'], Decimal('177.500'))

