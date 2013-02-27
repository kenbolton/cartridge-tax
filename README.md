#DO NOT USE IN PRODUCTION!

This repository is of educational and historical interest only.
The basic functionality of this app was added to [Cartridge](http://cartridge.jupo.org/) at version [0.8.0](https://github.com/stephenmcd/cartridge/tree/0.8.0).

The [TaxCloud.net](http://taxcloud.net/) integration may become a separate Cartridge app in the future.

#cartridge_tax

An implementation of sales tax for [Cartridge](http://cartridge.jupo.org/). 

A flat sales or value-added tax can be applied to in-state or all sales. Tax can optionally be applied to shipping costs.

For US-based sites, [TaxCloud.net](http://taxcloud.net/)'s tax lookup web service is optional. 

## DISCLAIMER

This should work out-of-the-box for simple cases. However, your particular implementation
of Cartridge may require rewriting this or merging components into or out of other projects.

## Installation

Working in your project's [virtualenv](http://www.virtualenv.org/en/latest/index.html):
```
pip install cartridge-tax
```
or
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
            "cartridge.shop.models.Order.tax_total",
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

An example for the US is at `cartridge_tax.forms.USOrderForm`. This
implementation uses the two-letter state abbreviation, so put e.g. NY as
the value of `TAX_SHOP_STATE` in /admin/conf/settings/. Add to
your `settings.py`:
`SHOP_CHECKOUT_FORM_CLASS = 'cartridge_tax.forms.USOrderForm'`

`USOrderForm` can be used as an example for developing `OrderForm`
subclasses for other tax jurisdictions.

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


