from product_feed_generator.modules.final_feed_.output.xml import (
    _add_products_to_final_feed,
)
from product_feed_generator.modules.final_feed_.output.database import (
    _save_custom_calc_units_to_database,
    _remove_custom_calc_unit_from_database,
    _sync_feed_conf_from_database,
)


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
