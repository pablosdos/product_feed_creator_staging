import string
import random
import json
from django.utils.safestring import mark_safe 
from product_feed_generator.models import (
    Feed,
    FeedConfiguration,
    Product
)
OPERATORS = [
    ("+", "+"),
    ("-", "-"),
    ("*", "*"),
    ("/", "/"),
    ("custom_value", "Custom Value – "),
]

def _save_custom_calc_units_to_database(custom_calculation_units_list, feed_conf_from_current_shop_for_updating, FeedConfiguration, feed_from_current_shop_for_filtering) -> dict:
    char_set = string.ascii_uppercase + string.digits
    random_placeholder = "placeholder_" + ''.join(random.sample(char_set*6, 6))
    json_ = {
        "custom_calc_field_name": random_placeholder,
        "calculation_elements": [],
    }
    custom_calculation_units_list.append(json_)
    custom_calculation_units_list_as_json_for_database = json.dumps(
        custom_calculation_units_list
    )
    # print(custom_calculation_units_list_as_json_for_database)
    feed_conf_from_current_shop_for_updating.update(
        custom_calculation_units_list=custom_calculation_units_list_as_json_for_database
    )
    feed_conf_from_current_shop = FeedConfiguration.objects.get(
        feed=feed_from_current_shop_for_filtering
    )
    return {"CustomCalcUnitsJson": mark_safe(feed_conf_from_current_shop.custom_calculation_units_list)}

def _remove_custom_calc_unit_from_database(customCalcUnitIndexToRemove, feed_conf_from_current_shop_for_updating):
    feed_conf_being_updated = feed_conf_from_current_shop_for_updating[0]
    custom_calculation_units_list_being_updated = json.loads(feed_conf_from_current_shop_for_updating[0].custom_calculation_units_list)
    custom_calculation_units_list_being_updated.pop(int(customCalcUnitIndexToRemove))
    updated_custom_calculation_units_list_for_html = custom_calculation_units_list_being_updated
    custom_calculation_units_list_for_being_saved_to_database = json.dumps(custom_calculation_units_list_being_updated)
    feed_conf_being_updated.custom_calculation_units_list = custom_calculation_units_list_being_updated
    feed_conf_from_current_shop_for_updating.update(
        custom_calculation_units_list=custom_calculation_units_list_for_being_saved_to_database
    )
    return {"CustomCalcUnitsJson": mark_safe(custom_calculation_units_list_being_updated), "CustomCalcUnits": updated_custom_calculation_units_list_for_html}

def _sync_feed_conf_from_database(request, shop_name):
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
    if shop_name == "Serverkast":
        allFieldsOfProduct = Product._meta.fields[:]
    elif shop_name == "TopSystems":
        allFieldsOfProduct = Product._meta.fields[:]
    elif shop_name == "IngramMicro":
        allFieldsOfProduct = Product._meta.fields[:]
    availableFieldsList = []
    for field in allFieldsOfProduct:
        availableFieldsList.append(field.name)
    availableFieldsList.pop(0)
    if current_product_schema_for_final_feed == []:
        finalFeedSchemaFieldsList = []
    else:
        finalFeedSchemaFieldsList = json.loads(
            current_product_schema_for_final_feed
        ).keys()
    custom_calculation_units_list = json.loads(
        feed_conf_from_current_shop.custom_calculation_units_list
    )
    # print(json.mark_safe(feed_conf_from_current_shop.custom_calculation_units_list))
    context.update({"CustomCalcUnits": custom_calculation_units_list}),
    context.update({"CustomCalcUnitsJson": mark_safe(feed_conf_from_current_shop.custom_calculation_units_list)}),
    context.update({"feeds": feeds}),
    context.update({"shop_name": shop_name}),
    context.update({"availableFields": availableFieldsList}),
    context.update(
        {"current_product_schema_for_final_feed": finalFeedSchemaFieldsList}
    )
    context.update({"operators": OPERATORS}),
    return context