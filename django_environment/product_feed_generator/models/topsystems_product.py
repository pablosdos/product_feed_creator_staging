from django.db import models

class TopSystemsProduct(models.Model):
    # one of many Serverkast_Products for one Feed | if Feed is deleted, Serverkast_Products from this Feed as well
    feed = models.ForeignKey(
        "Feed", on_delete=models.CASCADE, blank=False, null=False
    )
    is_selected = models.BooleanField()
    sku = models.CharField(max_length=63, verbose_name='MPN (originally SKU)')
    name = models.CharField(max_length=65535)
    short_desc = models.CharField(max_length=65535)
    long_description = models.CharField(max_length=65535)
    shipping_weight = models.DecimalField(max_digits=7, decimal_places=2)
    main_image = models.URLField(max_length=511, null=True, blank=True)
    extra_image_1 = models.URLField(max_length=511, null=True, blank=True)
    sales_price_excluding_tax = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Gross Price – calculated from original Price')
    brand = models.CharField(max_length=63)
    ean = models.CharField(max_length=63)
    current_stock = models.CharField(max_length=63)
    url_more_info = models.URLField(max_length=511)
    shipmentby = models.CharField(max_length=63)

    def __str__(self):
        return f"{self.name}"
    
    class Meta: 
        verbose_name = "Top Systems Product"
        verbose_name_plural = "Imported Top Systems Products"