import json
from decimal import Decimal
from product_feed_generator.models import (
    Feed,
    FeedConfiguration,
    Serverkast_Product,
    TopSystemsProduct,
)


def _apply_configuration_scheme(selected_products_list, shop_name) -> list:
    """
    Receive a list of products.

    Returns configured list of products.
    """
    feed_from_current_shop = Feed.objects.get(shop_name=shop_name)
    current_product_schema_for_final_feed = FeedConfiguration.objects.get(
        feed=feed_from_current_shop
    ).product_schema_for_final_feed
    current_product_schema_for_final_feed = json.loads(
        current_product_schema_for_final_feed
    ).keys()
    if shop_name == "Serverkast":
        allFieldsOfProduct = Serverkast_Product._meta.fields[:]
    elif shop_name == "TopSystems":
        allFieldsOfProduct = TopSystemsProduct._meta.fields[:]
    allOriginalAttributesOfList = []
    for field in allFieldsOfProduct:
        allOriginalAttributesOfList.append(field.name)
    attributes_to_remove_from_list = set(allOriginalAttributesOfList) - set(
        current_product_schema_for_final_feed
    )
    attributes_to_remove_from_list.add('feed_id')
    selected_products_list_with_custom_calc_fields = _add_custom_calc_fields(
        selected_products_list, allFieldsOfProduct, shop_name
    )
    for product in selected_products_list:
        product.update({"source_feed": shop_name})
        for attribute_to_remove in attributes_to_remove_from_list:
            if attribute_to_remove in product:
                del product[attribute_to_remove]
    return selected_products_list_with_custom_calc_fields


def _get_calculation_results(product, custom_field_with_name_and_parts) -> dict:
    """
    Receive Product-Object.
    Receive name and elements (also list) for the custom calculation field of the current feed as a list.

    Returns custom calc field name with calculated value (as dict) for updating product.
    """
    custom_calc_fields_as_return_value = {}
    temp_context_update = {}
    custom_calculated_field_name = ""
    custom_calculated_field_result_value = ""
    custom_field_with_name_and_parts_json = json.loads(custom_field_with_name_and_parts)
    for custom_field_with_name_and_parts in custom_field_with_name_and_parts_json:
        custom_calculated_field_name = custom_field_with_name_and_parts[
            "custom_calc_field_name"
        ]
        if len(custom_field_with_name_and_parts["calculation_elements"]) == 1:
            try:
                temp_context_update = {
                    custom_calculated_field_name: custom_field_with_name_and_parts["calculation_elements"][0].split("custom_value_")[1],
                }
            except:
                temp_context_update = {
                    custom_calculated_field_name: "value invalid",
                }
        else:
            string_for_evaluation_in_python = ""
            for calculation_element in custom_field_with_name_and_parts["calculation_elements"]:       
                if any(ext in calculation_element for ext in ["+", "-", "*", "/"]):
                    string_for_evaluation_in_python = string_for_evaluation_in_python + calculation_element
                elif "custom_value_" in calculation_element:
                    string_for_evaluation_in_python = (
                        string_for_evaluation_in_python
                        + "Decimal("
                        + calculation_element.split("custom_value_")[1]
                        + ")"
                    )
                else:
                    string_for_evaluation_in_python = (
                        string_for_evaluation_in_python + "product.get('" + calculation_element + "')"
                    )        
            try:
                custom_calculated_field_result_value = eval("round(" + string_for_evaluation_in_python + ",2)")
                temp_context_update = {
                    custom_calculated_field_name: custom_calculated_field_result_value,
                }
                custom_field_with_name_and_parts
            except:
                temp_context_update = {
                    custom_calculated_field_name: "calculation invalid",
                }
        custom_calc_fields_as_return_value.update(temp_context_update),
    return custom_calc_fields_as_return_value

def _add_custom_calc_fields(
    selected_products_list, allFieldsOfProduct, shop_name
) -> list:
    """
    Recieve product list (list of dicts).

    Add every custom calc field (calculated value) of fitting configurations to the list.

    Returns updated product list (list of dicts).
    """
    #
    # TODO – implement
    # get calculation from conf of shop_name and calculate from allFieldsOfProduct
    # finally create and add the custom field to selected_products_list
    #
    feed_from_current_shop = Feed.objects.get(shop_name=shop_name)
    custom_calculation_units_list = FeedConfiguration.objects.get(
        feed=feed_from_current_shop
    ).custom_calculation_units_list
    updated_selected_products_list = None
    for product in selected_products_list:
        product.update(_get_calculation_results(product, custom_calculation_units_list))
    return selected_products_list
