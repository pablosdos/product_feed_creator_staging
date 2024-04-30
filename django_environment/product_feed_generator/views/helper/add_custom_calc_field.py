"""
OUTDATED
SINCE
240131
NOT IN USE !
"""

from decimal import Decimal
from product_feed_generator.models import (
    Feed,
    FeedConfiguration,
)


def _get_calculation_result(custom_field_with_name_and_parts):
    custom_calculated_field_1_name = custom_field_with_name_and_parts[0]
    custom_calculated_field_1_parts = custom_field_with_name_and_parts[1:]
    string_for_evaluation_in_python = ""
    for part in custom_calculated_field_1_parts:
        if any(ext in part for ext in ["+", "-", "*", "/"]):
            string_for_evaluation_in_python = string_for_evaluation_in_python + part
        elif "custom_value_" in part:
            string_for_evaluation_in_python = (
                string_for_evaluation_in_python
                + "Decimal("
                + part.split("custom_value_")[1]
                + ")"
            )
        else:
            string_for_evaluation_in_python = (
                string_for_evaluation_in_python + "product.get('" + part + "')"
            )
    string_for_evaluation_in_python = "round(" + string_for_evaluation_in_python + ",2)"
    # print(string_for_evaluation_in_python)
    return {"field_name": custom_calculated_field_1_name, "eval_string": string_for_evaluation_in_python}


def add_custom_calc_field(selected_products_list, allFieldsOfProduct, shop_name):
    #
    # TODO – implement
    # get calculation from conf of shop_name and calculate from allFieldsOfProduct
    # finally create and add the custom field to selected_products_list
    #
    feed_from_current_shop = Feed.objects.get(shop_name=shop_name)
    # CUSTOM CALC FIELD 1
    custom_calculated_field_1_name_and_parts = FeedConfiguration.objects.get(
        feed=feed_from_current_shop
    ).custom_calculated_field_1.split("-")
    calc_result = _get_calculation_result(custom_calculated_field_1_name_and_parts)
    # print(calc_result)
    for product in selected_products_list:
        try:
            product.update(
                {calc_result['field_name']: eval(calc_result['eval_string'])}
            )
        except:
            product.update({calc_result['field_name']: "calculation_invalid"})
            # print('not working')
    return selected_products_list
