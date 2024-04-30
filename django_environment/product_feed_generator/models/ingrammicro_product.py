from django.db import models

class IngramMicroProduct(models.Model):
    # one of many IngramMicro_Products for one Feed | if Feed is deleted, Serverkast_Products from this Feed as well
    feed = models.ForeignKey(
        "Feed", on_delete=models.CASCADE, blank=False, null=False
    )
    is_selected = models.BooleanField()
    ingram_part_number = models.CharField(max_length=63)
    ingram_part_description = models.CharField(max_length=127)
    long_description = models.CharField(max_length=2055)
    brand = models.CharField(max_length=63)
    ean = models.CharField(max_length=63)
    current_stock = models.CharField(max_length=63)

    def __str__(self):
        return f"{self.ingram_part_description}"
    
    class Meta: 
        verbose_name = "Ingram Micro Product"
        verbose_name_plural = "Imported Ingram Micro Products"