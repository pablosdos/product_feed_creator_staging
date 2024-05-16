from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from product_feed_generator.models import Feed


class FeedForm(ModelForm):
    MY_CHOICES = (
        ("SELECT", "SELECT"),
        ("XML-URL", ".xml"),
        ("CSV-URL", ".csv"),
    )
    products_update_cronjob_active = forms.BooleanField(
        widget=forms.HiddenInput(), required=False
    )
    auto_add_new_products_cronjob_active = forms.BooleanField(
        widget=forms.HiddenInput(), required=False
    )
    input_type = forms.ChoiceField(choices=MY_CHOICES)
    products_last_updated = forms.CharField(
        widget=forms.HiddenInput(), required=False
    )
    available_fields = forms.CharField(
        widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super(FeedForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Feed
        fields = [
            "shop_name",
            "input_url",
            "input_type",
            "available_fields",
            "products_last_updated",
            "products_update_cronjob_active",
            "auto_add_new_products_cronjob_active",
        ]

        widgets = {"products_last_updated": forms.DateTimeInput()}

    def clean_shop_name(self):
        shop_name = self.cleaned_data['shop_name']
        print(shop_name)
        if Feed.objects.filter(shop_name=shop_name).exists():
            raise ValidationError("Feed name %a already exists" % (shop_name))
        return shop_name

    def clean(self):
        if (
            self.cleaned_data['input_type'] == 'SELECT'
        ):
            self.add_error(
                "input_type",
                "Please select an input file format",
            )
        return self.cleaned_data