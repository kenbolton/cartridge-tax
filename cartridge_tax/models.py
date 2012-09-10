from decimal import Decimal

from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import settings

from cartridge.shop.models import Order, SelectedProduct

from taxcloudapi import TaxCloudClient


def setup(self, request):
    """
    Set order fields that are stored in the session, item_total, tax_total,
    and total based on the given cart, and copy the cart items to the order.
    Called in the final step of the checkout process prior to the payment
    handler being called.
    """
    self.key = request.session.session_key
    self.user_id = request.user.id
    for field in self.session_fields:
        if field in request.session:
            setattr(self, field, request.session[field])
    self.total = self.item_total = request.cart.total_price()
    if self.shipping_total is not None:
        self.shipping_total = Decimal(str(self.shipping_total))
        self.total += self.shipping_total
    if self.discount_total is not None:
        self.total -= self.discount_total
    if self.total_tax is not None:
        self.total += self.total_tax
    self.save()  # We need an ID before we can add related items.
    for item in request.cart:
        product_fields = [f.name for f in SelectedProduct._meta.fields]
        item = dict([(f, getattr(item, f)) for f in product_fields])
        self.items.create(**item)

Order.setup = setup

