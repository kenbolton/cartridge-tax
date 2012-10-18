from django.contrib.localflavor.us.forms import USStateSelect

from cartridge.shop import checkout
from cartridge.shop.forms import OrderForm

from mezzanine.conf import settings


class USOrderForm(OrderForm):
    def __init__(self, request, step, *args, **kwrds):
        first = step == checkout.CHECKOUT_STEP_FIRST
        super(OrderForm, self).__init__(request, step, *args, **kwrds)
        if settings.SHOP_CHECKOUT_STEPS_SPLIT:
            if first:
                self.fields['billing_detail_state'].widget = USStateSelect()
                self.fields['shipping_detail_state'].widget = USStateSelect()
