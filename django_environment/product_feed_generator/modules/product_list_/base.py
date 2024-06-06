

from product_feed_generator.modules.product_list_.import_ import csv_file, sftp_server_file, xml_page
from product_feed_generator.models import Feed, Product, FeedConfiguration


class ProductList_:
    """
    This class handles everything in terms of the internal product list

    Returns None, since Views should collect their context themselves
    """
    @staticmethod
    def import_products_of_shop(shop_name: str):
        feed_from_current_shop: Feed = Feed.objects.get(shop_name=shop_name)
        feed_conf_from_current_shop: FeedConfiguration = FeedConfiguration.objects.get(feed=feed_from_current_shop)
        feedFormat: str = feed_from_current_shop.input_type
        if feedFormat == "CSV-URL":
            csv_file(feed=feed_from_current_shop, feed_conf=feed_conf_from_current_shop)
        if feedFormat == "SFTP-URL":
            sftp_server_file(feed=feed_from_current_shop, feed_conf=feed_conf_from_current_shop)
        if feedFormat == "XML-URL":
            xml_page(feed=feed_from_current_shop, feed_conf=feed_conf_from_current_shop)









