from django import forms
from product_feed_generator.models import FeedConfiguration


class SortingSelectForm(forms.Form):
    CHOICES = (
        ("Sort by", "Sort by"),
        ("A - Z ↑", "A - Z ↑"),
        ("A - Z ↓", "A - Z ↓"),
        ("Price ↑", "Price ↑"),
        ("Price ↓", "Price ↓"),
    )
    sorting_options = forms.ChoiceField(choices=CHOICES, widget = forms.Select(attrs = {'onchange' : "form.submit();"}))

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-select form-select-sm form-select-solid w-150px me-5'