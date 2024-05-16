# ✗ pipenv run python manage.py shell

from product_feed_generator.models import Serverkast_Product, TopSystemsProduct
from product_feed_generator.models import FeedConfiguration, Feed

Serverkast_Product.objects.all().delete()
topsystemsfeed = Feed.objects.get(shop_name="TopSystems")
FeedConfiguration.objects.create(
    feed=feed_xyz, product_schema_for_final_field="", custom_calculation_units_list=""
)
feed_conf_from_current_shop_for_updating = FeedConfiguration.objects.filter(
    feed=feed_xyz
)
