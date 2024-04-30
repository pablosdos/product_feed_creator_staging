from django.db import models

"""
    TODO-FFC –
    ADD GENERIC 
    FINAL FEED 
    PRODUCT MODEL
"""
class FinalFeedProduct(models.Model):
    sku = models.CharField(max_length=63)
    name = models.CharField(max_length=127)
    short_desc = models.CharField(max_length=127)
    long_description = models.CharField(max_length=2055)
    sales_price_excluding_tax = models.DecimalField(max_digits=6, decimal_places=2)
    brand = models.CharField(max_length=63)
    ean = models.CharField(max_length=63)
    current_stock = models.CharField(max_length=63)
    url_more_info = models.URLField(max_length=511)
    shipmentby = models.CharField(max_length=63)

    def __str__(self):
        return f"{self.name}"