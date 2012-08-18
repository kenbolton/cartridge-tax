from decimal import Decimal

from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import settings

from cartridge.shop.utils import set_shipping

from cartridgetax.utils import set_salestax

def default_billship_handler(request, order_form):
    """
    My planned US implementation will feature the ability to use either the
    local rate or the rate at the shipping address. A sketch of this
    implementation follows.

    Create the following settings in a module's defaults.py:
    * TAX_SHIPPING_ADDRESS boolean
    * TAX_API_KEY e.g. api.taxcloud.net for the US
    * TAX_RATE decimal, for just paying local sales tax
    * TAX_DISCOUNT_CATEGORIES list of shop Categories, e.g. Clothing which is
        sometimes taxed at a discount rate in NYC
    * TAX_DISCOUNT_RATE decimal percent discount for discounted categories

    Add 'taxable' BooleanField to the Product model through EXTRA_MODEL_FIELDS.
    Write a billship_handler that ties it all together.

    """    
    """
    Default billing/shipping handler - called when the first step in
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

    if not request.session.get('tax_shipping_address'):
        settings.use_editable()
        set_salestax(request, _("Flat sales tax"),
                request.cart.total_price() * Decimal(settings.TAX_FLAT_RATE))
    #else:
        #settings.use_editable()
        #set_salestax(request, _('Tax shipping address'),
                #tax_calculator(request.cart.
