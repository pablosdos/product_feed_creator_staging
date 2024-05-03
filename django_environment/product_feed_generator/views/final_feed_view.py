from django.template.loader import get_template
from django.http import HttpResponse
import xmltodict
import urllib.request
from urllib.request import Request
import json
from dicttoxml import dicttoxml
# from product_feed_generator.models import Serverkast_Product
from django.contrib.auth.decorators import login_required
from django.conf import settings

@login_required
def final_feed_view(request):
    if "clear_final_feed_submit" in request.POST:
        xml = dicttoxml({}, custom_root='product_final_feed', attr_type=False)
        f =  open(settings.LOCATION_OF_FINAL_FEED_FILE, "wb")
        f.write(xml)
        f.close()
        context = {"message": 'File is cleared'}
        template = get_template("final_feed_page.html")
        return HttpResponse(template.render(context, request))
    if request.method == "GET":
        context = {}
        template = get_template("final_feed_page.html")
        return HttpResponse(template.render(context, request))