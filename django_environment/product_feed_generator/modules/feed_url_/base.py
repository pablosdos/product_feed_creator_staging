import requests
import os
import csv
import io
import urllib.request
from urllib.parse import urlsplit, urlparse
import paramiko
# getAllFeedFields()
from urllib.request import Request
import xmltodict

from product_feed_generator.models import Product

request_header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "Accept-Encoding": "none",
    "Accept-Language": "en-US,en;q=0.8",
    "Connection": "keep-alive",
}


class FeedUrl_:
    """
    This class handles everything in terms of the Feed URL
    """
    @staticmethod
    def getFeedFormat(feedUrl: str):
        if urlsplit(feedUrl).scheme == "sftp":
            return "SFTP-URL"
        headers = requests.head(feedUrl).headers
        downloadable = "attachment" in headers.get("Content-Disposition", "")
        if downloadable:
            format_of_file = urllib.request.urlopen(feedUrl).info()["content-type"]
            if "csv" in format_of_file:
                return "CSV-URL"
            else:
                return "NOT-VALID-FEED-URL"
        else:
            path: str = urlsplit(feedUrl).path
            extension = os.path.splitext(path)[-1]
            if extension == ".xml":
                return "XML-URL"
            else:
                return "NOT-VALID-FEED-URL"

    @staticmethod
    def getAllFeedFields(feedUrl: str, feedFormat: str):
        if feedFormat == "XML-URL":
            feed_request = Request(feedUrl, headers=request_header)
            file = urllib.request.urlopen(feed_request)
            data = file.read()
            file.close()
            data = xmltodict.parse(data)
            products_list: list = data["rss"]["channel"]["item"]
            list_of_attribute_amounts = [len(item) for item in products_list]
            largest_amount_of_product_attributes_in_1_product: int = max(
                list_of_attribute_amounts
            )
            for item in products_list:
                if len(item) == largest_amount_of_product_attributes_in_1_product:
                    all_attributes_of_item: list = list(item)
            # print(all_attributes_of_item)
            return all_attributes_of_item
        if feedFormat == "CSV-URL":
            feed_request = Request(feedUrl, headers=request_header)
            file = urllib.request.urlopen(feed_request)
            csvfile = csv.reader(
                io.StringIO(file.read().decode("utf-8")), delimiter=","
            )
            data = list(csvfile)
            all_attributes_of_item: list = []
            for item in data[0]:
                all_attributes_of_item.append(item)
            return all_attributes_of_item
        if feedFormat == "SFTP-URL":
            parsed_url = urlparse(feedUrl)
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
            all_attributes_of_item: list = []
            with open("price.csv", "r") as csvfile:
                csvfile = csv.reader(csvfile)
                data = list(csvfile)
            for column_name in data[0]:
                all_attributes_of_item.append(column_name)
            return all_attributes_of_item