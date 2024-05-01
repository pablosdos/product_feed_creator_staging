from django import template
from product_feed_generator.models import Serverkast_Product, TopSystemsProduct, IngramMicroProduct, Product
import requests

register = template.Library()


@register.filter(name="is_url_image", is_safe=True)
def isUrlImage(image_url):
   image_formats = ("image/png", "image/jpeg", "image/jpg")
   r = requests.head(image_url)
   if r.headers["content-type"] in image_formats:
      return True
   return False

@register.filter(name="clear_if_placeholder", is_safe=True)
def clearIfPlaceholder(value):
    if "placeholder_" in value:
        return ""
    else:
        return value

@register.simple_tag
def tag_get_product_data(id_with_feed_source):
    django_product_id = id_with_feed_source.split(" ––– ")[0]
    source_feed = id_with_feed_source.split(" ––– ")[1]
    django_product_object = Product.objects.get(id=django_product_id)
    # if source_feed == "Serverkast":
    #     django_product_object = Serverkast_Product.objects.get(id=django_product_id)
    # elif source_feed == "TopSystems":
    #     django_product_object = TopSystemsProduct.objects.get(id=django_product_id)
    # elif source_feed == "IngramMicro":
    #     django_product_object = IngramMicroProduct.objects.get(id=django_product_id)
    return {
        "properties" : django_product_object,
        "id" : django_product_id
    }

