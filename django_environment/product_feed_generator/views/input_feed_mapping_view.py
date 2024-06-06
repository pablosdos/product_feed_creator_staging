import json

from django.template.loader import get_template
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required

from product_feed_generator.forms import *
from product_feed_generator.models import Feed, FeedConfiguration, Product
from product_feed_generator.modules.final_feed_.base import FinalFeed_
from product_feed_generator.modules import ProductList_

OPERATORS = [
    ("+", "+"),
    ("-", "-"),
    ("*", "*"),
    ("/", "/"),
    ("custom_value", "Custom Value – "),
]


@login_required
def input_feed_mapping_view(request, shop_name):
    """
    Default
    dynamic
    configuration
    page data
    added to
    context
    """
    request_post_body = request.POST
    # print(request_post_body)
    context = {}
    feeds = Feed.objects.all()
    feed_from_current_shop_for_filtering = Feed.objects.get(shop_name=shop_name)
    feed_from_current_shop_for_updating = Feed.objects.filter(shop_name=shop_name)
    try:
        feed_conf_from_current_shop = FeedConfiguration.objects.get(
            feed=feed_from_current_shop_for_filtering
        )
        feed_conf_from_current_shop_for_updating = FeedConfiguration.objects.filter(
            feed=feed_from_current_shop_for_filtering
        )
    except:
        feed_conf_from_current_shop = FeedConfiguration.objects.create(
            feed=feed_from_current_shop_for_filtering,
            product_schema_for_final_feed='{"name":"short_desc"}',
            custom_calculation_units_list='[{"custom_calc_field_name":"retail_price_excluding_tax","calculation_elements":["sales_price_excluding_tax","/","custom_value_121","*","custom_value_100"]},{"custom_calc_field_name":"cost_price","calculation_elements":["sales_price_excluding_tax","*","custom_value_0.65"]}]',
        )
        feed_conf_from_current_shop_for_updating = FeedConfiguration.objects.filter(
            feed=feed_from_current_shop_for_filtering
        )
    current_product_schema_for_final_feed: str = FeedConfiguration.objects.get(
        feed=feed_from_current_shop_for_filtering
    ).product_schema_for_final_feed
    current_product_schema_for_final_feed: dict = json.loads(
        current_product_schema_for_final_feed
    )

    availableFieldsList: list = json.loads(
        feed_from_current_shop_for_filtering.available_fields
    )
    # print(availableFieldsList)
    if current_product_schema_for_final_feed == []:
        finalFeedSchemaFieldsList = []
    else:
        finalFeedSchemaFieldsList = current_product_schema_for_final_feed

    custom_calculation_units_list = json.loads(
        feed_conf_from_current_shop.custom_calculation_units_list
    )
    # print(type(current_product_schema_for_final_feed))
    context.update({"feeds": feeds}),
    context.update({"shop_name": shop_name}),
    context.update({"availableFields": availableFieldsList}),

    context.update(
        {"current_product_schema_for_final_feed": current_product_schema_for_final_feed}
    ),
    context.update({"operators": OPERATORS}),
    template = get_template("input_feed_mapping_page.html")
    # provide for IngramMicro additionally credentials_form
    initial = {
        # "xml_user": feed_conf_from_current_shop.xml_user,
        # "xml_pass": feed_conf_from_current_shop.xml_pass,
        # "sftp_url": feed_conf_from_current_shop.sftp_url,
    }
    credentials_form = SftpXmlCredentialsForm(initial)
    context.update({"credentials_form": credentials_form}),

    product_fields: list = [f.name for f in Product._meta.get_fields()]
    product_fields.pop(0)
    product_fields.pop(0)
    product_fields.pop(0)

    context.update({"product_fields": product_fields}),

    """
    Add changed
    configurations
    to database
    """
    if "save-schema-config" in request_post_body:
        feed_conf_from_current_shop_for_updating.update(
            product_schema_for_final_feed=request_post_body.get(
                "finalFeedProductSchemaWithoutCustomCalcUnits", "[]"
            )
        )
        # finalfeed = FinalFeed_(shop_name)
        # context = finalfeed.sync_from_database(request)
        # del finalfeed
        current_product_schema_for_final_feed: str = FeedConfiguration.objects.get(
            feed=feed_from_current_shop_for_filtering
        ).product_schema_for_final_feed
        current_product_schema_for_final_feed: dict = json.loads(
            current_product_schema_for_final_feed
        )
        context.update(
            {"current_product_schema_for_final_feed": current_product_schema_for_final_feed}
        ),
        if feed_from_current_shop_for_updating[0].is_new_feed == True:
            context.update({"update_message": "Feed created 🎉"}),
            feed_from_current_shop_for_updating.update(is_new_feed=False)
        else:
            context.update({"update_message": "Mapping updated"}),
    # print(context)

    if "load-products-from-source" in request_post_body:
        ProductList_.import_products_of_shop(shop_name)
        context.update({"update_message": "Sync done"}),

    if feed_from_current_shop_for_updating[0].is_new_feed == True:
        context.update({"is_new_feed": True}),

    return HttpResponse(template.render(context, request))
