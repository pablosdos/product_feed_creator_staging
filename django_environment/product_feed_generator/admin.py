from django.contrib import admin
from django import forms
from .models import Feed, FeedConfiguration, Product


class FeedForm(forms.ModelForm):
    MY_CHOICES = (
        ("XML-URL", ".xml-URL"),
        ("CSV-URL", ".csv-URL"),
        ("SOMETHING-ELSE", "something-else"),
    )

    input_type = forms.ChoiceField(choices=MY_CHOICES)


class FeedAdmin(admin.ModelAdmin):
    readonly_fields = ("input_type",)

    fields = (
        "shop_name",
        "input_url",
        "input_type",
        "available_fields",
        "products_last_updated",
        "products_update_cronjob_active",
        "auto_add_new_products_cronjob_active",
        "is_new_feed",
    )
    list_display = (
        "shop_name",
        "input_type",
    )
    form = FeedForm


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        # "name",
        # "brand",
        "feed",
        "is_selected",
    )


admin.site.register(Feed, FeedAdmin)
admin.site.register(FeedConfiguration)
admin.site.register(Product, ProductAdmin)
