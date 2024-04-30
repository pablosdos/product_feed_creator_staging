from django import forms
from product_feed_generator.models import IngramMicroProduct

class IngramMicroProductSelectForFinalFeedForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(IngramMicroProductSelectForFinalFeedForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        """
        Add one form field
        for every product
        of the Product Model
        """
        """
        TODO – IMPLEMENT PAGINATION
        FOR DEMO JUST FIRST 1000 PRODUCTS
        """
        for i, q in enumerate(IngramMicroProduct.objects.all()[0:1000]):
            # has to be identical to field in product_feed_generator/views/product_selection_view.py
            self.fields["%s ––– %s"%(q.ean,q.ingram_part_description)] = forms.BooleanField(required=False)