from django.http import HttpRequest

from product_feed_generator.modules.final_feed_.output.xml import (
    _add_products_to_final_feed,
)
from product_feed_generator.modules.final_feed_.output.database import (
    _save_custom_calc_units_to_database,
    _remove_custom_calc_unit_from_database,
    _sync_feed_conf_from_database,
)
from product_feed_generator.models import (
    Product,
)


@staticmethod
def handle_selection_of_products(request: HttpRequest):
    selected_products_from_database_list: list[Product] = Product.objects.filter(
        is_selected=True
    )
    # select product
    for form_product in request.POST:
        if " ––– " in form_product:
            product_name_of_form = form_product.split(" ––– ")[1]
            Product.objects.filter(name=product_name_of_form).update(is_selected=True)
    # unselect product
    # selected_products_from_form_list: list = []
    # for value in request.POST:
    #     selected_products_from_form_list.append(str(value))
    # for db_product in selected_products_from_database_list:
    #     # contnains substring (if not it was unselected)? If not unselect
    #     if not any(str(db_product) in s for s in selected_products_from_form_list):
    #         Product.objects.filter(name=db_product).update(is_selected=False)


class FinalFeed_:
    """
    This class handles everything in terms of the Final Feed
    """

    # def __init__(_self):
    # self._shop_name = name
    # _self.shop_name = shop_name

    def save_xml_file(_self, unconfigured_product_list) -> dict:
        """
        Saves XML file containing selected products from every feed.

        And returns a dict with the context, used for the http response (presentation of the page):
        Feed infos, updated products, the form and information message.

        """
        # print(_self.shop_name)
        return _add_products_to_final_feed(unconfigured_product_list)

    def save_to_database(
        _self,
        custom_calculation_units_list,
        feed_conf_from_current_shop_for_updating,
        FeedConfiguration,
        feed_from_current_shop_for_filtering,
    ) -> dict:
        return _save_custom_calc_units_to_database(
            custom_calculation_units_list,
            feed_conf_from_current_shop_for_updating,
            FeedConfiguration,
            feed_from_current_shop_for_filtering,
        )

    def remove_from_database(
        _self, customCalcUnitIndexToRemove, feed_conf_from_current_shop_for_updating
    ) -> dict:
        return _remove_custom_calc_unit_from_database(
            customCalcUnitIndexToRemove, feed_conf_from_current_shop_for_updating
        )

    def sync_from_database(_self, request) -> dict:
        return _sync_feed_conf_from_database(request, _self.shop_name)
