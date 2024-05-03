from django.contrib import admin
from django.urls import path
from .views import master_list_view, input_feed_mapping_view

urlpatterns = [
    path('', master_list_view, name='master_list_page'),
    # path('feeds/<str:shop_name>', product_selection_view, name='product_selection_page'),
    path('feeds/<str:shop_name>/input-feed-mapping', input_feed_mapping_view, name='input_feed_mapping_page'),
    # path('final-feed', final_feed_view, name='final_feed_page'),
    # path('final-feed-xml', final_feed_xml_view, name='final_feed_xml_page'),
]

admin.site.site_header = 'Feed Fusion Administration'