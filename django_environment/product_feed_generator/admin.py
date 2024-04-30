from django.contrib import admin
from django import forms
from .models import (
    Feed,
    FeedConfiguration,
    Serverkast_Product,
    TopSystemsProduct,
    IngramMicroProduct,
    Product
)


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
        "products_last_updated",
        "products_update_cronjob_active",
    )
    list_display = (
        "shop_name",
        "input_type",
    )
    form = FeedForm


class ServerkastProductAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)
    list_display = ("id", "name", "is_selected")


class TopSystemsProductAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)
    list_display = ("id", "name", "is_selected")


class IngramMicroProductAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)
    list_display = ("id", "ingram_part_description", "is_selected")


admin.site.register(Feed, FeedAdmin)
admin.site.register(FeedConfiguration)
admin.site.register(Serverkast_Product, ServerkastProductAdmin)
admin.site.register(TopSystemsProduct, TopSystemsProductAdmin)
admin.site.register(IngramMicroProduct, IngramMicroProductAdmin)
admin.site.register(Product)
