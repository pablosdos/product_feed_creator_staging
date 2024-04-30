from django import forms
from product_feed_generator.models import FeedConfiguration

class FeedConfigForm(forms.Form):
    retail_price_excluding_tax_division_value = forms.DecimalField()
    retail_price_excluding_tax_multiplication_value = forms.DecimalField()
    cost_price_multiplication_value = forms.DecimalField()
