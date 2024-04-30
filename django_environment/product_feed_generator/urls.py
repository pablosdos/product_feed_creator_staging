from django.urls import path
from .views import *

urlpatterns = [
    path('', feed_selection_view, name='feed_selection_page'),
    path('feeds/<str:shop_name>', product_selection_view, name='product_selection_page'),
    path('feeds/<str:shop_name>/manage-imports', manage_product_import_view, name='manage_product_import_page'),
    path('final-feed', final_feed_view, name='final_feed_page'),
    # path('final-feed-xml', final_feed_xml_view, name='final_feed_xml_page'),
]
