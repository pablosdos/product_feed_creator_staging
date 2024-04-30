"""
Request all products
from the shops product list
and import them
to the database
"""
from urllib.request import Request
from product_feed_generator.models import Feed, Serverkast_Product, IngramMicroProduct
from urllib.parse import urlparse
import paramiko
from decimal import Decimal
import csv
from django.template.loader import get_template
from product_feed_generator.forms import *
from product_feed_generator.views.helper.get_legacy_session import get_availability

def from_ingrammicro_feed(request, shop_name):
    feed_from_current_shop = Feed.objects.get(shop_name=shop_name)
    feed_conf_from_current_shop = FeedConfiguration.objects.get(
        feed=feed_from_current_shop
    )
    form_for_final_feed_products = IngramMicroProductSelectForFinalFeedForm()
    # initial = {
    #     "xml_user": feed_conf_from_current_shop.xml_user,
    #     "xml_pass": feed_conf_from_current_shop.xml_pass,
    #     "sftp_url": feed_conf_from_current_shop.sftp_url,
    # }
    """
    Request the products
    providing the protection credentials
    and save the products
    to database
    """
    parsed_url = urlparse(feed_conf_from_current_shop.sftp_url)
    # hostname=str(parsed_url.hostname)
    hostname = str(parsed_url.hostname)
    username = str(parsed_url.username)
    password = str(parsed_url.password)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=hostname,
        username=username,
        password=password,
        allow_agent=False,
        look_for_keys=False,
    )
    sftp = client.open_sftp()
    sftp.get("PRICE.TXT", "price.csv")
    # filename = "price_dummy.csv"
    filename = "price.csv"
    IngramMicroProduct.objects.all().delete()
    product_list = []
    with open(filename, "r") as csvfile:
        datareader = csv.reader(csvfile)
        # skip first line (header)
        next(datareader)
        for row in datareader:
            ingram_part_number_for_xml_request = row[0]
            # get availability from xml request
            # in_stock = get_availability(ingram_part_number_for_xml_request)
            # print(in_stock)
            product_list.append(
                IngramMicroProduct(
                    feed=feed_from_current_shop,
                    is_selected=False,
                    ingram_part_number=row[0],
                    ingram_part_description=row[1],
                    long_description=row[12],
                    brand=row[5],
                    ean=row[3],
                    current_stock='0',
                )
            )
    # print(product_list)
    IngramMicroProduct.objects.bulk_create(product_list)

    sftp.close()
    # return the context
    context = {
        "feed": feed_from_current_shop,
        "form": form_for_final_feed_products,
    }
    return context


# [0'additional_imagelinks,1"brand",2"categories",3"category",4"color",5"condition",6"delivery",7"description",8"ean",9"gender",10"id",11"image_link",12"is_in_stock",13"item_group_id",14"korting",15"link",16"manage_stock",17"material",18"max_price",19"min_price",20"min_sale_qty",21"price",22"prijs_amazon",23"product_type",24"qty_increments",25"shipping_weight",26"size",27"sku",28"special_price",29"special_price_from",30"special_price_to",31"status",32"stock",33"title",34"type",35"type_bootuitrusting",36"verzending",37"visibility"']


def extract_and_save_products_with_password(request, shop_name):
    if shop_name == "IngramMicro":
        context = from_ingrammicro_feed(request, shop_name)
    return context
