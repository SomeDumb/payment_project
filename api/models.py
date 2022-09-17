from django.db import models
from django.utils.translation import gettext as _
import stripe
import pprint
class Item(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Название предмета"))
    description = models.TextField(verbose_name=_("Описание"))
    
    def get_prices(self, *args, **kwargs):
        """
        Return related prices.
        """
        
        prices = {i.currency:i.price for i in self.price_set.all()}
        return prices
    
    @staticmethod
    def archive_product(product, price):
        """
        Archives product and price with given id
        """
        stripe.Product.modify(product, active=False)
        stripe.Price.modify(price, active=False)
    
    def create_product(self, unit_amount, currency_options, *args, **kwargs):
        product = stripe.Product.create(
            name=self.name, description=self.description,
            default_price_data={
                "unit_amount_decimal":unit_amount,
                "currency":"rub",
                "currency_options": currency_options
            }
        )
        return product
    
    def create_or_update_stripe(self, *args, **kwargs):
        """
        Function to get product price if exists, overwise create one. Updates price of product on stripe if needed.
            Returns: 
                created
                stripe_price
        """

        stripe_products = stripe.Product.search(query=f"name:'{self.name}' AND \
            description:'{self.description}' AND active:'true'",)

        db_prices = {}

        for price in self.price_set.all():
            db_prices[price.currency]={"unit_amount_decimal":str(price.price)}
            
        db_currency_options = {i:db_prices[i] for i in db_prices if i!='rub'} # Currency options without main currency (rub).
        
        if stripe_products['data']: 
            # Product exists, update price if needed.

            product = stripe_products['data'][0]
            pprint.pprint(product)
            stripe_price = stripe.Price.retrieve(product['default_price'], expand=['currency_options'])
            if stripe_price['unit_amount_decimal']!=str(db_prices['rub']['unit_amount_decimal']):
                # Default price on stripe is not up-to-date. Creates new product with new price.
                try:
                    self.archive_product(product['id'], stripe_price['id'])
                except Exception as e:
                    print(e)
                
                try:
                    product = self.create_product(str(db_prices['rub']["unit_amount_decimal"]), db_currency_options)
                except Exception as e:
                    print('creation failed', e)
                    
                stripe_price = product['default_price']
            else:
                # Default price is up to date, updates currency_options if needed.
                
                try:
                    stripe_currency_options = stripe_price['currency_options']
                    stripe_currency_options = {
                        i:{'unit_amount_decimal':stripe_currency_options[i]['unit_amount_decimal']} for i in stripe_currency_options
                    }
                    
                    if stripe_currency_options!=db_prices:
                        self.archive_product(product['id'], stripe_price['id'])
                        product = self.create_product(str(db_prices['rub']["unit_amount_decimal"]), db_currency_options)
                        stripe_price = product['default_price']
                    
                except Exception as e:
                    print('default is up to date', e)
            created = False
        else:
            # Product with given name and description not exist, creates one.
            product = self.create_product(str(db_prices['rub']["unit_amount_decimal"]), db_currency_options)
            pprint.pprint(product)
            stripe_price = product['default_price']
            created = True
            
        return created, stripe_price
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Предмет')
        verbose_name_plural = _("Предметы")

class Price(models.Model):
    price = models.BigIntegerField(verbose_name=_("Цена"))
    currency = models.CharField(max_length=3, verbose_name=_("Валюта"))
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.currency
    
    class Meta:
        verbose_name = _('Цена')
        verbose_name_plural = _("Цены")
    
class Order(models.Model):
    items = models.ManyToManyField(Item, verbose_name=_("Предметы"))
    class Meta:
        verbose_name = _('Заказ')
        verbose_name_plural = _("Заказы")