# ✗ pipenv run python manage.py shell

from product_feed_generator.models import IngramMicroProduct, Serverkast_Product, TopSystemsProduct

Serverkast_Product.objects.all().delete()