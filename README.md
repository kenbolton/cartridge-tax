#cartridge_tax
An implementation of sales tax for [Cartridge](http://cartridge.jupo.org/). 

A flat sales or value-added tax can be applied to in-state or all sales. Tax can optionally be applied to shipping costs.

For US-based sites, [TaxCloud.net](http://taxcloud.net/)'s tax lookup web service is optional. An experimental integration of TaxCloud's tax authorization and capture exists.

## DISCLAIMER

This should work out-of-the-box for simple cases. However, your particular implementation
of Cartridge may require rewriting this or merging components into or out of other projects.

## Installation

Working in your project's [virtualenv](http://www.virtualenv.org/en/latest/index.html):

```
git clone https://github.com/kenbolton/cartridge-tax.git
cd cartridge-tax
python setup.py install
```

Add `'cartridge_tax'` to your settings.INSTALLED_APPS before
`'cartridge.shop'`.

Set up your tax information in the admin configuration settings,
/admin/conf/setting/. Note the value you put in 'Shop State'. You will
need to inject a "choices" dict into
`cartridge.shop.forms.OrderForm['fields']['shipping_detail_state']`. The
values in that dict should match the style in 'Shop State'. See the
example below in `Custom OrderForm`.

### Billing/Shipping and Order Handlers

Add the following to your settings:
```
SHOP_HANDLER_BILLING_SHIPPING = \
                "cartridge_tax.checkout.tax_billship_handler"

SHOP_HANDLER_ORDER = "cartridge_tax.checkout.tax_order_handler"
```

### Extra model fields

Below is an example of settings.EXTRA_MODEL_FIELDS. Be sure to add these
tuples to your own EXTRA_MODEL_FIELDS.

```
EXTRA_MODEL_FIELDS = (
        (
            "cartridge.shop.models.Product.tic",
            "CharField",
            (u"Taxability Information Code",),
            {"max_length":"5", "blank": True, "default":"00000", },
            ),
        (
            "cartridge.shop.models.Order.total_tax",
            "DecimalField",
            (u"Tax Total",),
            {"null": True, "blank": True, "max_digits": 10,
                    "decimal_places": 2},
            ),
        (
            "cartridge.shop.models.Order.tax_type",
            "CharField",
            (u"Tax Type",),
            {"blank": True, "max_length": "20", "default":"Flat sales tax"},
            ),
)
```

### Custom OrderForm
An example for the US.

Assuming your app is named `app`, add `SHOP_CHECKOUT_FORM_CLASS = 'app.forms.OrderForm'`
to settings. Create `app/forms.py`, and fill with:

```
class OrderForm(OrderForm):
    def __init__(self, request, step, *args,**kwrds):
        first = step == checkout.CHECKOUT_STEP_FIRST
        super(OrderForm, self).__init__(request, step, *args, **kwrds)
        if settings.SHOP_CHECKOUT_STEPS_SPLIT:
            if first:
                self.fields['billing_detail_state'].widget = USStateSelect()
                self.fields['shipping_detail_state'].widget = USStateSelect()
```

## Registered Settings

* TAX_SHOP_ADDRESS
* TAX_SHOP_ADDRESS2
* TAX_SHOP_CITY
* TAX_SHOP_STATE
* TAX_SHOP_POSTCODE
* TAX_SHOP_POSTCODE_PLUS4
* TAX_OUT_OF_STATE
* TAX_FLAT_RATE
* TAX_SHIPPING_ADDRESS
* TAX_SHIPPING
* TAX_USE_TAXCLOUD
* TAX_USE_TAXCLOUD_AUTHORIZATION
* TAX_TAXCLOUD_API_ID
* TAX_TAXCLOUD_API_KEY


