from django import forms
from product_feed_generator.models import Serverkast_Product, TopSystemsProduct

class ServerkastProductSelectForFinalFeedForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ServerkastProductSelectForFinalFeedForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        """
        Add one form field
        for every product
        of the Product Model
        """
        for i, q in enumerate(Serverkast_Product.objects.all()[0:10]):
            # has to be identical to field in product_feed_generator/views/product_selection_view.py
            self.fields["%s ––– %s"%(q.ean,q.name)] = forms.BooleanField(required=False)