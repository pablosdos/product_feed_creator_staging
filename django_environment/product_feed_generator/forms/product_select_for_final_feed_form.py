from django import forms

class ProductSelectForFinalFeedForm(forms.Form):
    def __init__(self, page_of_products, *args, **kwargs):
        super(ProductSelectForFinalFeedForm, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        """
        Add one form field
        for every product
        of the Product Model
        """
        for index, product in enumerate(page_of_products):
            self.fields["%s ––– %s"%(product.id,product.feed)] = forms.BooleanField(required=False)
