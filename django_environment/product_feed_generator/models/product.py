from django.db import models

class Product(models.Model):
    feed = models.ForeignKey(
        "Feed", on_delete=models.CASCADE, blank=False, null=False
    )
    is_selected = models.BooleanField()
    # sku = models.CharField(max_length=65535, verbose_name='MPN (originally SKU)')
    sku = models.CharField(max_length=65535)
    name = models.CharField(max_length=65535)
    short_desc = models.CharField(max_length=65535)
    long_description = models.CharField(max_length=65535)
    shipping_weight = models.CharField(max_length=65535)
    main_image = models.CharField(max_length=65535)
    extra_image_1 = models.CharField(max_length=65535)
    sales_price_excluding_tax = models.FloatField(max_length=65535, null=True, blank=True)
    brand = models.CharField(max_length=65535)
    ean = models.CharField(max_length=65535)
    current_stock = models.CharField(max_length=65535)
    url_more_info = models.CharField(max_length=65535)
    shipmentby = models.CharField(max_length=65535)

    def __str__(self):
        return f"{self.name}"
    
    class Meta: 
        verbose_name = "Product"
        verbose_name_plural = "Imported Products"