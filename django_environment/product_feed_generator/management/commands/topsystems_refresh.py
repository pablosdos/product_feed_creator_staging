# #!/usr/bin/python3

from django.core.management.base import BaseCommand
from urllib.request import Request
import urllib.request
import csv
import io
from datetime import datetime
from decimal import Decimal
from .email_output_helper import *
from product_feed_generator.models import Feed, Serverkast_Product, TopSystemsProduct

class Command(BaseCommand):
    help = "Sends emails"

    def handle(self, *args, **kwargs):
        shop_name = "TopSystems"
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
            csvfile = csv.reader(io.StringIO(file.read().decode("utf-8")), delimiter=",")
            header = next(csvfile)
            TopSystemsProduct.objects.all().delete()
            # print(header)
            data = list(csvfile)
            # print(data)
            for item in data:
                price_original = Decimal(item[21].split(" EUR")[0].strip(' "'))
                sales_price_excluding_tax = ( price_original  / 121 ) * 100
                TopSystemsProduct.objects.create(
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
            now = datetime.now()
            Feed.objects.filter(shop_name=shop_name).update(products_last_updated=now)