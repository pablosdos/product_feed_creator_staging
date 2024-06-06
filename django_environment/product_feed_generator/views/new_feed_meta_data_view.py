from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from datetime import date
import ast
import json
from product_feed_generator.forms import FeedForm
from product_feed_generator.models import FeedConfiguration, Feed
from product_feed_generator.modules import FeedUrl_


# @method_decorator(csrf_exempt, name='dispatch')
@login_required
def new_feed_meta_data_view(request):
    context: dict = {}
    request_post = request.POST
    # print(request_post)
    if "inputURLInputFieldPhantomForSending" in request_post:
        input_url: str = request_post.get("inputURLInputFieldPhantomForSending")
        feed_format: str = FeedUrl_.getFeedFormat(input_url)
        input_fields: str = FeedUrl_.getAllFeedFields(input_url, feed_format)
        # input_fields = '["additional_imagelinks", "brand", "material", "min_price", "min_sale_qty", "price", "max_price", "prijs_amazon", "product_type", "qty_increments", "shipping_weight", "size", "sku", "special_price", "special_price_from",  "special_price_to", "status", "stock",  "title", "type", "type_bootuitrusting",  "verzending", "visibility"]'
        form = FeedForm(
            initial={
                "shop_name": request_post.get("shopNameInputFieldPhantomForSending"),
                "input_type": feed_format,
                "input_url": input_url,
            }
        )
        context["form"] = form
        context["input_fields_js_array"] = mark_safe(input_fields)
        if feed_format == "NOT-VALID-FEED-URL":
            context["input_url_alert"] = "This is not a valid Feed Input URL"
        return render(request, "new_feed_meta_data_page.html", context)

    if "nextBtn" in request_post:
        form = FeedForm(request.POST or None, request.FILES or None)
        # SFTP-URL
        if form.is_valid():
            form_ = form.save(commit=False)
            shop_name: str = form.cleaned_data["shop_name"]
            form_.available_fields = "[" + form.cleaned_data["available_fields"] + "]"
            form_.products_update_cronjob_active = False
            form_.auto_add_new_products_cronjob_active = False
            form_.is_new_feed = True
            form_.products_last_updated = date.today()
            form.save()
            return redirect("input_feed_mapping_page", shop_name=shop_name)

    form = FeedForm(request.POST or None, request.FILES or None)
    context["form"] = form
    # pass empty string, so JavaScript in template doesn´t break
    context["input_fields_js_array"] = mark_safe([])
    return render(request, "new_feed_meta_data_page.html", context)
