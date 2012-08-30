# Cartridgetax

An implementation of tax for Cartridge using the TaxCloud.net api.

## Billing/Shipping Handler

Add the following to your settings:
```
SHOP_HANDLER_BILLING_SHIPPING = \
                "cartridgetax.checkout.tax_billship_handler"
```

## Extra model fields

Below is an example of settings.EXTRA_MODEL_FIELDS. Be sure to add these
tuples to your own customized EXTRA_MODEL_FIELDS.
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
