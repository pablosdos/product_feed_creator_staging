"""
OUTDATED
SINCE
240131
NOT IN USE !
"""

# from decimal import Decimal

# def apply_topsystems_configuration_scheme(complete_topsystems_products_list):
#     for product in complete_topsystems_products_list:
#         product['retail_price_excluding_tax'] = round(( product.get('sales_price_excluding_tax')  / 121 ) * 100, 2)
#         product['cost_price'] = round(product.get('retail_price_excluding_tax') * Decimal(0.65), 2)
#     return complete_topsystems_products_list

# def apply_serverkast_configuration_scheme(complete_serverkast_products_list):
#     for product in complete_serverkast_products_list:
#         product['retail_price_excluding_tax'] = round( product.get('sales_price_excluding_tax')* Decimal(1.15), 2)
#         product['cost_price'] = round(product.get('sales_price_excluding_tax') * Decimal(0.85), 2)
#     return complete_serverkast_products_list


import copy
import json
from decimal import Decimal
from product_feed_generator.models import (
    Feed,
    FeedConfiguration,
    Serverkast_Product,
    TopSystemsProduct,
)
from .add_custom_calc_field import *

def apply_configuration_scheme(selected_products_list, shop_name):
    # print(selected_products_list)
    #1 find attributes to remove
    #filter list
    feed_from_current_shop = Feed.objects.get(shop_name=shop_name)
    # current_product_schema_for_final_feed = FeedConfiguration.objects.get(
    #     feed=feed_from_current_shop
    # ).product_schema_for_final_feed.split(",")
    current_product_schema_for_final_feed = FeedConfiguration.objects.get(
        feed=feed_from_current_shop
    ).product_schema_for_final_feed
    current_product_schema_for_final_feed = json.loads(current_product_schema_for_final_feed).keys()

    
    #original attributes list
    if shop_name == "Serverkast":
        allFieldsOfProduct = Serverkast_Product._meta.fields[:]
    elif shop_name == "TopSystems":
        allFieldsOfProduct = TopSystemsProduct._meta.fields[:]
    allOriginalAttributesOfList = []
    for field in allFieldsOfProduct:
        allOriginalAttributesOfList.append(field.name)
    attributes_to_remove_from_list = set(allOriginalAttributesOfList) - set(current_product_schema_for_final_feed)
    #2 clean products by filter list
    # print(attributes_to_remove_from_list)
    selected_products_list_with_custom_calc_field = add_custom_calc_field(selected_products_list, allFieldsOfProduct, shop_name)
    # print(selected_products_list_with_custom_calc_field)

    for product in selected_products_list:
        for attribute_to_remove in attributes_to_remove_from_list:
            if attribute_to_remove in product:
                del product[attribute_to_remove]
    
    return selected_products_list_with_custom_calc_field

