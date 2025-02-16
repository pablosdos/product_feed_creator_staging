"""
Request all products
from the shops product list
and import them
to the database
"""

from urllib.request import Request
from product_feed_generator.models import Feed, Product
import urllib.request
import xmltodict
import csv
import json
import io
from decimal import Decimal
from django.template.loader import get_template
from product_feed_generator.forms import *

request_header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "Accept-Encoding": "none",
    "Accept-Language": "en-US,en;q=0.8",
    "Connection": "keep-alive",
}


def from_serverkast_feed(request, shop_name):
    feed = Feed.objects.get(shop_name=shop_name)
    site = feed.input_url
    feed_request = Request(site, headers=request_header)
    file = urllib.request.urlopen(feed_request)
    data = file.read()
    file.close()
    data = xmltodict.parse(data)
    products = data["rss"]["channel"]["item"]
    # Serverkast_Product.objects.all().delete()
    new_product_list = []
    product_data = {}
    """
    Check the new
    RSS Feed of
    the Shop
    """
    for item in products:
        if not ("gross_price" in item):
            pass
            # print('item gross price is empty for')
            # print(item["name"])
        else:
            product_data = {
                "feed": feed,
                "is_selected": False,
                "sku": item["sku"],
                "name": item["name"],
                "short_desc": item.get("short_desc", "empty"),
                "long_description": item.get("long_description", "empty"),
                "main_image": item["main_image"],
                "extra_image_1": item.get("extra_image_1", None),
                "extra_image_2": item.get("extra_image_2", None),
                "extra_image_3": item.get("extra_image_3", None),
                "extra_image_4": item.get("extra_image_4", None),
                "extra_image_5": item.get("extra_image_5", None),
                "extra_image_6": item.get("extra_image_6", None),
                "extra_image_7": item.get("extra_image_7", None),
                "extra_image_8": item.get("extra_image_8", None),
                "extra_image_9": item.get("extra_image_9", None),
                "sales_price_excluding_tax": item["gross_price"],
                "brand": item["brand"],
                "ean": item.get("ean", "empty"),
                "current_stock": item["current_stock"],
                "url_more_info": item["url_more_info"],
                "shipmentby": item.get("shipmentby", "unknown"),
            }
            new_product_list.append(Product(**product_data))
    old_products = Product.objects.all()
    old_products_names = [old_product.name for old_product in old_products]
    new_products_names = [new_product.name for new_product in new_product_list]
    list_of_newly_added_product_names = []
    """
    Compare old (from database)
    and new product names
    """
    for new_product_name in new_products_names:
        if new_product_name not in old_products_names:
            list_of_newly_added_product_names.append(new_product_name)
    """
    Remove the database
    products and replace
    it with updated ones
    (select new products)
    """
    Product.objects.all().delete()
    for item in products:
        if not ("gross_price" in item):
            pass
            # print('item gross price is empty for')
            # print(item["name"])
        else:
            product_data = {
                "feed": feed,
                "is_selected": False,
                "sku": item["sku"],
                "name": item["name"],
                "short_desc": item.get("short_desc", "empty"),
                "long_description": item.get("long_description", "empty"),
                "main_image": item["main_image"],
                "extra_image_1": item.get("extra_image_1", None),
                "extra_image_2": item.get("extra_image_2", None),
                "extra_image_3": item.get("extra_image_3", None),
                "extra_image_4": item.get("extra_image_4", None),
                "extra_image_5": item.get("extra_image_5", None),
                "extra_image_6": item.get("extra_image_6", None),
                "extra_image_7": item.get("extra_image_7", None),
                "extra_image_8": item.get("extra_image_8", None),
                "extra_image_9": item.get("extra_image_9", None),
                "sales_price_excluding_tax": item["gross_price"],
                "brand": item["brand"],
                "ean": item.get("ean", "empty"),
                "current_stock": item["current_stock"],
                "url_more_info": item["url_more_info"],
                "shipmentby": item.get("shipmentby", "unknown"),
            }
            Product.objects.create(**product_data)
    for newly_added_product_name in list_of_newly_added_product_names:

        product_for_update = Product.objects.get(name=newly_added_product_name)
        product_for_update.is_selected = True
        product_for_update.save()
    return request


def from_topsystems_feed(request, shop_name):
    feed = Feed.objects.get(shop_name=shop_name)
    site = feed.input_url
    feed_request = Request(site, headers=request_header)
    file = urllib.request.urlopen(feed_request)
    csvfile = csv.reader(io.StringIO(file.read().decode("utf-8")), delimiter=",")
    header = next(csvfile)
    new_product_list = []
    # print(header)
    data = list(csvfile)
    # print(data)
    """
    Check the new
    CSV Feed of
    the Shop
    """
    for item in data:
        sales_price_excluding_tax = Decimal(item[21].split(" EUR")[0].strip(' "'))
        product_data = {
            "feed":feed,
            "is_selected":False,
            "sku":item[27],
            "name":item[33],
            "long_description":item[7],
            "main_image":item[11],
            "extra_image_1":item[0],
            "sales_price_excluding_tax":sales_price_excluding_tax,
            "shipping_weight":Decimal(item[25].split(" kg")[0].strip(' "')),
            "brand":item[1],
            "ean":item[8],
            "current_stock":item[32],
        }
        new_product_list.append(Product(**product_data))
    file.close()
    # print(all_new_created_products)
    form = ProductSelectForFinalFeedForm()
    # print(form)
    context = {
        "feed": feed,
        "form": form,
    }
    old_products = Product.objects.all()
    old_products_names = [old_product.name for old_product in old_products]
    new_products_names = [new_product.name for new_product in new_product_list]
    list_of_newly_added_product_names = []
    """
    Compare old (from database)
    and new product names
    """
    # print(old_products_names)
    # print(new_products_names)
    for new_product_name in new_products_names:
        if new_product_name not in old_products_names:
            print(new_product_name)
            list_of_newly_added_product_names.append(new_product_name)
    print(list_of_newly_added_product_names)
    """
    Remove the database
    products and replace
    it with updated ones
    (select new products)
    """
    Product.objects.all().delete()
    for item in data:
        sales_price_excluding_tax = Decimal(item[21].split(" EUR")[0].strip(' "'))
        product_data = {
            "feed":feed,
            "is_selected":False,
            "sku":item[27],
            "name":item[33],
            "long_description":item[7],
            "main_image":item[11],
            "extra_image_1":item[0],
            "sales_price_excluding_tax":sales_price_excluding_tax,
            "shipping_weight":Decimal(item[25].split(" kg")[0].strip(' "')),
            "brand":item[1],
            "ean":item[8],
            "current_stock":item[32],
        }
        Product.objects.create(**product_data)
    # print(TopSystemsProduct.objects.get(name='MG SmartLink Connect'))
    for newly_added_product_name in list_of_newly_added_product_names:
        product_for_update = Product.objects.get(name=newly_added_product_name)
        product_for_update.is_selected = True
        product_for_update.save()
    return context


def from_ingrammicro_feed(request, shop_name):
    feed = Feed.objects.get(shop_name=shop_name)
    form = ProductSelectForFinalFeedForm()

    context = {
        "feed": feed,
        "form": form,
    }
    return context


# [0'additional_imagelinks,1"brand",2"categories",3"category",4"color",5"condition",6"delivery",7"description",8"ean",9"gender",10"id",11"image_link",12"is_in_stock",13"item_group_id",14"korting",15"link",16"manage_stock",17"material",18"max_price",19"min_price",20"min_sale_qty",21"price",22"prijs_amazon",23"product_type",24"qty_increments",25"shipping_weight",26"size",27"sku",28"special_price",29"special_price_from",30"special_price_to",31"status",32"stock",33"title",34"type",35"type_bootuitrusting",36"verzending",37"visibility"']


def add_new_products(request, shop_name):
    if shop_name == "Serverkast":
        request = from_serverkast_feed(request, shop_name)
    elif shop_name == "TopSystems":
        request = from_topsystems_feed(request, shop_name)
    elif shop_name == "IngramMicro":
        request = from_ingrammicro_feed(request, shop_name)
    return request
