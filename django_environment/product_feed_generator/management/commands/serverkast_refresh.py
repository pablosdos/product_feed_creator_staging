# #!/usr/bin/python3

from django.core.management.base import BaseCommand
from urllib.request import Request
import urllib.request
from datetime import datetime
import xmltodict
from .email_output_helper import *
from product_feed_generator.models import Feed, Serverkast_Product, TopSystemsProduct


class Command(BaseCommand):
    help = "Refresh Serverkast Products"

    def handle(self, *args, **kwargs):
        shop_name = "Serverkast"
        feed = Feed.objects.get(shop_name=shop_name)
        if feed.products_update_cronjob_active == True:
            site = feed.input_url
            hdr = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
                "Accept-Encoding": "none",
                "Accept-Language": "en-US,en;q=0.8",
                "Connection": "keep-alive",
            }
            feed_request = Request(site, headers=hdr)
            file = urllib.request.urlopen(feed_request)
            data = file.read()
            file.close()
            data = xmltodict.parse(data)
            items = data["rss"]["channel"]["item"]
            Serverkast_Product.objects.all().delete()
            for item in items:
                if not ("sales_price_excluding_tax" in item):
                    pass
                    # print('item gross price is empty for')
                    # print(item["name"])
                else:
                    Serverkast_Product.objects.create(
                        feed=feed,
                        is_selected=False,
                        sku=item["sku"],
                        name=item["name"],
                        short_desc=item.get("short_desc", "empty"),
                        long_description=item.get("long_description", "empty"),
                        main_image=item["main_image"],
                        extra_image_1=item.get("extra_image_1", None),
                        extra_image_2=item.get("extra_image_2", None),
                        extra_image_3=item.get("extra_image_3", None),
                        extra_image_4=item.get("extra_image_4", None),
                        extra_image_5=item.get("extra_image_5", None),
                        extra_image_6=item.get("extra_image_6", None),
                        extra_image_7=item.get("extra_image_7", None),
                        extra_image_8=item.get("extra_image_8", None),
                        extra_image_9=item.get("extra_image_9", None),
                        sales_price_excluding_tax=item["sales_price_excluding_tax"],
                        brand=item["brand"],
                        ean=item.get("ean", "empty"),
                        current_stock=item["current_stock"],
                        url_more_info=item["url_more_info"],
                        shipmentby=item.get("shipmentby", "unknown"),
                    )
            now = datetime.now()
            Feed.objects.filter(shop_name=shop_name).update(products_last_updated=now)