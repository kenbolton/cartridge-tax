# cartridge-tax

cartridge-tax is an implementation of sales tax for the light-weight Django
ecommerce application Cartridge. A flat sales or value-added tax can be 
applied to in-state or all sales.

Please fork!

## ToDo

The big pending feature is to calculate tax to the shipping address
using the TaxCloud.net api for US retailers.


## Installation

Clone (or fork!) this repository and run `python setup.py install `

uAdd `'cartridge-tax'` to your settings.INSTALLED_APPS before
`'cartridge.shop'`.

Set up your tax information in the admin configuration settings,
/admin/conf/setting/. Note the value you put in 'Shop State'. You will
need to inject a "choices" dict into
`cartridge.forms.OrderForm['fields']['shipping_detail_state']`. The
values in that dict should match the style in 'Shop State'.

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
        (
            "cartridge.shop.models.Order.total_tax",
            "cartridge.shop.fields.MoneyField",
            (u"Tax Total",),
            {},
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
* TAX_OUT_OF_STATE
* TAX_FLAT_RATE
* TAX_SHIPPING_ADDRESS
* TAX_SHIPPING
* TAX_USE_TAXCLOUD
* TAX_TAXCLOUD_API_ID
* TAX_TAXCLOUD_API_KEY


