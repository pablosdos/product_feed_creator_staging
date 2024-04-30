from django.db import models
from product_feed_generator.models import Feed

class FeedConfiguration(models.Model):
    feed = models.OneToOneField(
        Feed,
        on_delete=models.CASCADE,
    )
    retail_price_excluding_tax_division_value = models.DecimalField(max_digits=9, decimal_places=2)
    retail_price_excluding_tax_multiplication_value = models.DecimalField(max_digits=9, decimal_places=2)
    cost_price_multiplication_value = models.DecimalField(max_digits=9, decimal_places=2)
    product_schema_for_final_feed = models.TextField(max_length=1023, verbose_name='Product Schema For Final Field')
    custom_calculation_units_list = models.TextField(max_length=2055, verbose_name='Custom Calculation Units List')
    xml_user = models.CharField(max_length=63, null=True, blank=True)
    xml_pass = models.CharField(max_length=63, null=True, blank=True)
    sftp_url = models.CharField(max_length=127, null=True, blank=True)

    def __str__(self):
        return f"{self.feed} Configuration"
