"""
Request all products
from the shops product list
and import them
to the database
"""

import urllib.request
from urllib.request import Request
from product_feed_generator.models import Feed, Product

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
    feed_request = Request(feed.input_url, headers=request_header)
    file = urllib.request.urlopen(feed_request)
    data = file.read()
    file.close()
    data = xmltodict.parse(data)
    products_list: list = data["rss"]["channel"]["item"]
    Product.objects.all().delete()
    for item in products_list:
        if not ("gross_price" in item):
            pass
            # print('item gross price is empty for')
            # print(item["name"])
        else:
            sales_price_excluding_tax = Decimal(
                item["gross_price"].split(" EUR")[0].strip(' "')
            )
            Product.objects.create(
                feed=feed,
                is_selected=False,
                sku=item["sku"],
                name=item["name"],
                long_description=item.get(
                    "long_description", "description not available"
                ),
                main_image=item["main_image"],
                extra_image_1=item.get("extra_image_1", None),
                sales_price_excluding_tax=item["gross_price"],
                shipping_weight=Decimal(0.0),
                brand=item["brand"],
                ean=item.get("ean", "EAN not available"),
                current_stock=item["current_stock"],
            )
    # print(json.dumps(items[0], indent=4))
    form = ProductSelectForFinalFeedForm()
    # print(form)
    context = {
        "feed": feed,
        "form": form,
    }
    return context


def from_topsystems_feed(request, shop_name):
    feed = Feed.objects.get(shop_name=shop_name)
    site = feed.input_url
    feed_request = Request(site, headers=request_header)
    file = urllib.request.urlopen(feed_request)
    csvfile = csv.reader(io.StringIO(file.read().decode("utf-8")), delimiter=",")
    header = next(csvfile)
    Product.objects.all().delete()
    # print(header)
    data = list(csvfile)
    # print(data)
    for item in data:
        sales_price_excluding_tax = Decimal(item[21].split(" EUR")[0].strip(' "'))
        Product.objects.create(
            feed=feed,
            is_selected=False,
            sku=item[27],
            name=item[33],
            long_description=item[7],
            main_image=item[11],
            extra_image_1=item[0],
            sales_price_excluding_tax=sales_price_excluding_tax,
            shipping_weight=Decimal(item[25].split(" kg")[0].strip(' "')),
            brand=item[1],
            ean=item[8],
            current_stock=item[32],
        )
    file.close()
    # print(all_new_created_products)
    form = ProductSelectForFinalFeedForm()
    # print(form)
    context = {
        "feed": feed,
        "form": form,
    }
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

@staticmethod
def extract_and_save_products(page_of_products: int):

    existing_feeds: list[Feed] = Feed.objects.all()
    Product.objects.all().delete()

    for feed in existing_feeds:
        if feed.input_type == "XML-URL":
            feed_request = Request(feed.input_url, headers=request_header)
            file = urllib.request.urlopen(feed_request)
            data = file.read()
            file.close()
            data = xmltodict.parse(data)
            products_list: list = data["rss"]["channel"]["item"]

            for item in products_list:
                if not ("gross_price" in item):
                    pass
                    # print('item gross price is empty for')
                    # print(item["name"])
                else:
                    sales_price_excluding_tax = Decimal(
                        item["gross_price"].split(" EUR")[0].strip(' "')
                    )
                    Product.objects.create(
                        feed=feed,
                        is_selected=False,
                        sku=item["sku"],
                        name=item["name"],
                        long_description=item.get(
                            "long_description", "description not available"
                        ),
                        main_image=item["main_image"],
                        extra_image_1=item.get("extra_image_1", None),
                        sales_price_excluding_tax=item["gross_price"],
                        shipping_weight=Decimal(0.0),
                        brand=item["brand"],
                        ean=item.get("ean", "EAN not available"),
                        current_stock=item["current_stock"],
                    )

        if feed.input_type == "CSV-URL":
            feed_request = Request(feed.input_url, headers=request_header)
            file = urllib.request.urlopen(feed_request)
            csvfile = csv.reader(io.StringIO(file.read().decode("utf-8")), delimiter=",")
            data = list(csvfile)
            for item in data:
                # sales_price_excluding_tax = Decimal(item[21].split(" EUR")[0].strip(' "'))
                Product.objects.create(
                    feed=feed,
                    is_selected=False,
                    sku=item[27],
                    name=item[33],
                    long_description=item[7],
                    main_image=item[11],
                    extra_image_1=item[0],
                    sales_price_excluding_tax=sales_price_excluding_tax,
                    shipping_weight=30,
                    brand=item[1],
                    ean=item[8],
                    current_stock=item[32],
                )
            file.close()

    form = ProductSelectForFinalFeedForm(page_of_products)
    context = {
        "feed": feed,
        "form": form,
    }
    # if shop_name == "Serverkast":
    #     context = from_serverkast_feed(request, shop_name)
    # elif shop_name == "TopSystems":
    #     context = from_topsystems_feed(request, shop_name)
    # elif shop_name == "IngramMicro":
    #     context = from_ingrammicro_feed(request, shop_name)
    return context
