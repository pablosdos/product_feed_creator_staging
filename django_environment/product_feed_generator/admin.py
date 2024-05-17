from django.contrib import admin
from django import forms
from .models import Feed, FeedConfiguration, Product


class FeedForm(forms.ModelForm):
    MY_CHOICES = (
        ("XML-URL", ".xml-URL"),
        ("CSV-URL", ".csv-URL"),
    )

    input_type = forms.ChoiceField(choices=MY_CHOICES)


class FeedAdmin(admin.ModelAdmin):
    fields = (
        "shop_name",
        "input_url",
        "input_type",
        "available_fields",
        "products_last_updated",
        "products_update_cronjob_active",
        "auto_add_new_products_cronjob_active",
    )
    list_display = (
        "shop_name",
        "input_type",
    )
    form = FeedForm


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brand",
        "is_selected",
    )


admin.site.register(Feed, FeedAdmin)
admin.site.register(FeedConfiguration)
admin.site.register(Product, ProductAdmin)
