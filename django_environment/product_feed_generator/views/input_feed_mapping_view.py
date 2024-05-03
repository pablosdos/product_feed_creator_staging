from django.template.loader import get_template
from django.http import HttpResponse
import json
from product_feed_generator.modules.final_feed_.base import FinalFeed_
from django.utils.safestring import mark_safe 
from product_feed_generator.forms import *
from product_feed_generator.models import (
    Feed,
    FeedConfiguration,
    Product
)
from django.contrib.auth.decorators import login_required

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
    context = {}
    feeds = Feed.objects.all()
    feed_from_current_shop_for_filtering = Feed.objects.get(shop_name=shop_name)
    feed_conf_from_current_shop = FeedConfiguration.objects.get(
        feed=feed_from_current_shop_for_filtering
    )
    feed_conf_from_current_shop_for_updating = FeedConfiguration.objects.filter(
        feed=feed_from_current_shop_for_filtering
    )
    current_product_schema_for_final_feed = FeedConfiguration.objects.get(
        feed=feed_from_current_shop_for_filtering
    ).product_schema_for_final_feed
    allFieldsOfProduct = json.loads(feed_from_current_shop_for_filtering.available_fields) 
    # if shop_name == "Serverkast":
    #     allFieldsOfProduct = Serverkast_Product._meta.fields[:]
    # elif shop_name == "TopSystems":
    #     allFieldsOfProduct = TopSystemsProduct._meta.fields[:]
    # elif shop_name == "IngramMicro":
    #     allFieldsOfProduct = IngramMicroProduct._meta.fields[:]
    availableFieldsList = []
    for field in allFieldsOfProduct:
        availableFieldsList.append(field)
    availableFieldsList.pop(0)
    # print(availableFieldsList)
    if current_product_schema_for_final_feed == []:
        finalFeedSchemaFieldsList = []
    else:
        finalFeedSchemaFieldsList = json.loads(
            current_product_schema_for_final_feed
        ).keys()
    custom_calculation_units_list = json.loads(
        feed_conf_from_current_shop.custom_calculation_units_list
    )
    print(current_product_schema_for_final_feed)
    # print(json.mark_safe(feed_conf_from_current_shop.custom_calculation_units_list))
    context.update({"CustomCalcUnits": custom_calculation_units_list}),
    context.update({"CustomCalcUnitsJson": mark_safe(feed_conf_from_current_shop.custom_calculation_units_list)}),
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
        "xml_user": feed_conf_from_current_shop.xml_user,
        "xml_pass": feed_conf_from_current_shop.xml_pass,
        "sftp_url": feed_conf_from_current_shop.sftp_url,
    }
    credentials_form = SftpXmlCredentialsForm(initial)
    context.update({"credentials_form": credentials_form}),
    product_fields: list[str] = ["sku", "name", "short_desc", "long_description", "shipping_weight", "main_image", "extra_image_1", "sales_price_excluding_tax", "brand", "ean", "current_stock", "url_more_info", "shipmentby"]
    context.update({"product_fields": product_fields}),
    # adding custom calc field
    # if "add_custom_calc_field" in request.POST:
    #     finalfeed = FinalFeed_(shop_name)
    #     updated_custom_calc_units_for_context = finalfeed.save_to_database(custom_calculation_units_list, feed_conf_from_current_shop_for_updating, FeedConfiguration, feed_from_current_shop_for_filtering)
    #     context.update(updated_custom_calc_units_for_context)
    #     del finalfeed
    # if "remove_custom_calc_field" in request_post_body:
    #     finalfeed = FinalFeed_(shop_name)
    #     updated_custom_calc_units_for_context = finalfeed.remove_from_database(request_post_body.get("customCalcUnitIndex", ""), feed_conf_from_current_shop_for_updating)
    #     context.update(updated_custom_calc_units_for_context)
    #     del finalfeed
    # # save-protection-credentials
    # if "save-protection-credentials" in request_post_body:
    #     # print(request_post_body.get("xml_pass", ""))
    #     feed_conf_from_current_shop_for_updating.update(
    #         xml_user=request_post_body.get("xml_user", "")
    #     )
    #     feed_conf_from_current_shop_for_updating.update(
    #         xml_pass=request_post_body.get("xml_pass", "")
    #     )
    #     feed_conf_from_current_shop_for_updating.update(
    #         sftp_url=request_post_body.get("sftp_url", "")
    #     )
    #     context.update({"update_message": "Protection credentials updated!"}),
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
        feed_conf_from_current_shop_for_updating.update(
            custom_calculation_units_list=request_post_body.get(
                "finalFeedCustomCalcUnits", "[]"
            )
        )
        finalfeed = FinalFeed_(shop_name)
        # context = finalfeed.sync_from_database(request)
        del finalfeed
        context.update({"update_message": "Schema updated!"}),
    # print(context)
    return HttpResponse(template.render(context, request))
