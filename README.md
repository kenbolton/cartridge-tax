My planned US implementation will feature the ability to use either the local rate or the rate at the shipping address. A sketch of this implementation follows.

Create the following settings in a module's defaults.py:
* TAX_SHIPPING_ADDRESS boolean
* TAX_API_KEY e.g. api.taxcloud.net for the US
* TAX_RATE decimal, for just paying local sales tax
* TAX_DISCOUNT_CATEGORIES list of shop Categories, e.g. Clothing which is sometimes taxed at a discount rate in NYC
* TAX_DISCOUNT_RATE decimal percent discount for discounted categories

Add 'taxable' BooleanField to the Product model through EXTRA_MODEL_FIELDS.
Write a billship_handler that ties it all together.

