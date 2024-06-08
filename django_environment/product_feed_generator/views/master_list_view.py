import xmltodict
import urllib.request
from urllib.request import Request
import pprint
import json
from dicttoxml import dicttoxml

from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models.query import QuerySet
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from product_feed_generator.models import Feed, FeedConfiguration, Product
from product_feed_generator.views.helper import *
from product_feed_generator.modules.final_feed_.base import (
    handle_selection_of_products,
    FinalFeed_,
)
from product_feed_generator.modules.final_feed_.output.xml import (
    create_final_feed_xml_file,
)

# from product_feed_generator.modules.final_feed_.base import FinalFeed_
from product_feed_generator.forms import (
    ProductSelectForFinalFeedForm,
    SortingSelectForm,
)


@login_required
def master_list_view(request):
    object_list: QuerySet[Product] = Product.objects.all()
    if request.method == "POST":
        page_number = 1
        sort_type = request.POST.get("sorting_options", "Sort by")
        choosen_company: str = request.POST.get("feed_source_selector", "All")
        search_query: str = request.POST.get("search_bar", "")

    elif request.method == "GET":
        page_number = request.GET.get("page")
        sort_type = request.session["sort_type"]
        choosen_company: str = request.session["choosen_company"]
        search_query: str = request.session["search_query"]

    sorting_option_form = SortingSelectForm()
    # print(request.POST)
    if "add-to-product-collection-form" in request.POST:
        handle_selection_of_products(request)

    # filter by company
    object_list = object_list.filter(feed__shop_name__icontains=choosen_company)
    if choosen_company == "All":
        object_list = Product.objects.all()
    else:
        object_list = object_list
    request.session["choosen_company"] = choosen_company

    # search by search bar
    if "search_bar" is not "":
        object_list = object_list.filter(
            Q(name__icontains=search_query)
            | Q(short_desc__icontains=search_query)
            | Q(brand__icontains=search_query)
            | Q(ean__icontains=search_query)
        )
        request.session["search_query"] = search_query

    # make price sortable
    # for object in object_list:

    # sort by sort_type
    if sort_type == "Sort by":
        object_list = object_list
    if sort_type == "A - Z ↑":
        object_list = object_list.order_by("name")
    if sort_type == "A - Z ↓":
        object_list = object_list.order_by("-name")
    if sort_type == "Price ↑":
        object_list = object_list.order_by("sales_price_excluding_tax")
    if sort_type == "Price ↓":
        object_list = object_list.order_by("-sales_price_excluding_tax")
    request.session["sort_type"] = sort_type

    initial = {
        "sorting_options": sort_type,
        "feed_source_selector": choosen_company,
        "search_bar": search_query,
    }
    sorting_option_form = SortingSelectForm(initial=initial)

    paginator = Paginator(object_list, 50)

    paginator_control_with_products_queryset = paginator.get_page(page_number)
    paginated_form = ProductSelectForFinalFeedForm(
        paginator_control_with_products_queryset
    )

    """
    CONTEXT
    FOR PAGE
    """
    if sort_type != "":
        sort_type: str = "Sort by"
    feeds = Feed.objects.all()
    context = {
        # "feed": feed,
        "feeds": feeds,
        "found_products_count": paginator.count,
        "sort_type": sort_type,
        "sorting_option_form": sorting_option_form,
        "form": paginated_form,
        "paginator_control": paginator_control_with_products_queryset,
        # "feed_config_form": feed_config_form,
    }

    # export product list to .xml file
    if "trigger-export" is not "":
        create_final_feed_xml_file()

    template = get_template("master_list_page.html")
    return HttpResponse(template.render(context, request))
