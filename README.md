# cartridge-tax

An implementation of sales tax for Cartridge. A flat sales or
value-added tax can be applied. Please fork!

## ToDo

The big pending feature is to calculate tax to the shipping address
using the TaxCloud.net api for US retailers.


## Installation

Add `'cartridge-tax'` to your settings.INSTALLED_APPS.

### Billing/Shipping Handler

Add the following to your settings:
```
SHOP_HANDLER_BILLING_SHIPPING = \
                "cartridge-tax.checkout.tax_billship_handler"
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
        ),
        (
            "cartridge.shop.models.Order.total_tax",
            "MoneyField",
            (u"Tax Total",),
            ),
)
```


## Registered Settings

* TAX_SHOP_ADDRESS
* TAX_SHOP_ADDRESS2
* TAX_SHOP_CITY
* TAX_SHOP_STATE
* TAX_SHOP_POSTCODE
* TAX_SHOP_POSTCODE_PLUS4
* TAX_FLAT_RATE
* TAX_SHIPPING_ADDRESS
* TAX_SHIPPING
* TAX_TAXCLOUD_API_ID
* TAX_TAXCLOUD_API_KEY


