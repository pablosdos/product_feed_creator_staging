import csv
import io
import paramiko
from urllib.parse import urlparse
import urllib.request
import json
from decimal import Decimal
import xmltodict
from urllib.request import Request

from product_feed_generator.models import Feed, Product, FeedConfiguration

from django.conf import settings


def safe(value, default):
    return value or default


feed_fusion_product_model_attributes: list = [
    "sku",
    "name",
    "short_desc",
    "long_description",
    "shipping_weight",
    "shipping_weight",
    "main_image",
    "extra_image_1",
    "sales_price_excluding_tax",
    "brand",
    "ean",
    "current_stock",
    "url_more_info",
    "shipmentby",
]


def _import_list_file(product_data: list, feed: Feed, feed_conf: FeedConfiguration):
    if feed.input_type == "XML-URL":
        list_of_attribute_amounts = [len(item) for item in product_data]
        largest_amount_of_product_attributes_in_1_product: int = max(
            list_of_attribute_amounts
        )
        for item in product_data:
            if len(item) == largest_amount_of_product_attributes_in_1_product:
                all_attributes_of_item: list = list(item)
        # print(all_attributes_of_item)
    else:
        all_attributes_of_item: list = []
        for item in product_data[0]:
            all_attributes_of_item.append(item)
        product_data.pop(0)
    # 2) apply the schema on every product
    product_schema: dict = json.loads(feed_conf.product_schema_for_final_feed)
    product_list_for_storing: list = []
    for product in product_data:
        # 3) create vars (mapped attribute as value) for keys of Feed Fusion product model in the schema
        for feed_fusion_model_key, mapped_value in product_schema.items():
            # print(product)
            if feed.input_type == "XML-URL":
                # product is dict
                if mapped_value in product:
                    exec(
                        f'''{feed_fusion_model_key}: str = """ {product[mapped_value]} """'''
                    )
                else:
                    exec(
                        f'''{feed_fusion_model_key}: str = ""'''
                    )
            else:
                # product is list
                exec(
                    f'''{feed_fusion_model_key}: str = """{product[all_attributes_of_item.index(mapped_value)]}"""'''
                )
        # 4) if keys exists leave them, otherwise set to empty string
        for attribute in feed_fusion_product_model_attributes:
            try:
                exec(attribute)
            except:
                exec(f"{attribute} = None")

        product_list_for_storing.append(
            # 5) add attribute if part of the mapping, otherwise empty string
            Product(
                feed=feed,
                is_selected=False,
                sku=safe(locals()["sku"], ""),
                name=safe(locals()["name"], ""),
                short_desc=safe(locals()["short_desc"], ""),
                long_description=safe(locals()["long_description"], ""),
                shipping_weight=safe(locals()["shipping_weight"], ""),
                main_image=safe(locals()["main_image"], ""),
                extra_image_1=safe(locals()["extra_image_1"], ""),
                sales_price_excluding_tax=safe(
                    locals()["sales_price_excluding_tax"], ""
                ),
                brand=safe(locals()["brand"], ""),
                ean=safe(locals()["ean"], ""),
                current_stock=safe(locals()["current_stock"], ""),
                url_more_info=safe(locals()["url_more_info"], ""),
                shipmentby=safe(locals()["shipmentby"], ""),
            )
        )
    Product.objects.filter(feed=feed).delete()
    Product.objects.bulk_create(product_list_for_storing)
    return None


def xml_page(feed: Feed, feed_conf: FeedConfiguration):
    feed = Feed.objects.get(shop_name=feed.shop_name)
    feed_request = Request(feed.input_url, headers=settings.REQUEST_HEADER)
    file = urllib.request.urlopen(feed_request)
    data = file.read()
    file.close()
    data = xmltodict.parse(data)
    products_list: list = data["rss"]["channel"]["item"]
    _import_list_file(product_data=products_list, feed=feed, feed_conf=feed_conf)
    return None


def csv_file(feed: Feed, feed_conf: FeedConfiguration):
    feed_request = urllib.request.Request(
        feed.input_url, headers=settings.REQUEST_HEADER
    )
    file = urllib.request.urlopen(feed_request)
    csvfile = csv.reader(io.StringIO(file.read().decode("utf-8")), delimiter=",")
    # 1) get original attributes of products
    data: list = list(csvfile)
    _import_list_file(product_data=data, feed=feed, feed_conf=feed_conf)
    return None


def sftp_server_file(feed: Feed, feed_conf: FeedConfiguration):
    """
    Request the products
    and save the products
    to database
    """
    parsed_url = urlparse(feed.input_url)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=str(parsed_url.hostname),
        username=str(parsed_url.username),
        password=str(parsed_url.password),
        allow_agent=False,
        look_for_keys=False,
    )
    sftp = client.open_sftp()
    sftp.get("PRICE.TXT", "price.csv")
    # Product.objects.all().delete()
    # 1) get original attributes of products
    all_attributes_of_item: list = []
    with open("price.csv", "r") as file:
        csvfile = csv.reader(file)
        data: list = list(csvfile)
        _import_list_file(product_data=data, feed=feed, feed_conf=feed_conf)
    return None
