from product_feed_generator.models import (
    Feed,
)
from dicttoxml import dicttoxml
from django.template.loader import get_template
from django.db.models.query import QuerySet
from product_feed_generator.forms import *
from django.conf import settings
from product_feed_generator.modules.final_feed_.modify import (
    _apply_configuration_scheme,
)
from product_feed_generator.views.helper import *


def from_serverkast_feed(request, shop_name):
    feed = Feed.objects.get(shop_name=shop_name)
    # form = ServerkastProductSelectForFinalFeedForm(request.POST)
    form = SortingSelectForm()
    if feed.auto_add_new_products_cronjob_active:
        # print(request.POST)
        add_new_products(request, shop_name)
    """
    check
    products (in db)
    by
    form
    """
    if form.is_valid():
        for key, value in form.cleaned_data.items():
            product_name_of_form = key.split(" ––– ")[1]
            # Serverkast_Product.objects.filter(name=product_name_of_form).update(
            #     is_selected=value
            # )
            product_for_update = Serverkast_Product.objects.get(
                name=product_name_of_form
            )
            product_for_update.is_selected = value
            product_for_update.save()
    # xxx = Serverkast_Product.objects.filter(
    #     is_selected=True
    # ).values()
    # print(xxx)

    all_updated_products = Serverkast_Product.objects.all()
    template = get_template("master_list_page.html")
    # has to be identical to field in product_feed_generator/forms/serverkast_product_select_for_final_feed_form.py
    init = {
        "%s ––– %s" % (row.ean, row.name): row.is_selected
        for row in all_updated_products
    }
    # form = ServerkastProductSelectForFinalFeedForm(init)
    form = SortingSelectForm()
    context = {
        "feed": feed,
        "products": all_updated_products,
        "form": form,
        "message": "Products are added to Final Feed",
    }
    """
    create
    final
    feed
    from
    checked
    products (in db)
    """
    template = get_template("master_list_page.html")
    selected_products_from_topsystems_products_list = TopSystemsProduct.objects.filter(
        is_selected=True
    ).values()
    # print(selected_products_from_topsystems_products_list)
    complete_topsystems_products_list = [
        entry for entry in selected_products_from_topsystems_products_list
    ]
    configured_topsystems_products_list = _apply_configuration_scheme(
        complete_topsystems_products_list, "TopSystems"
    )
    selected_products_from_serverkast_products_list = Serverkast_Product.objects.filter(
        is_selected=True
    ).values()
    # print(selected_products_from_serverkast_products_list)
    # convert queryset to list
    complete_serverkast_products_list = [
        entry for entry in selected_products_from_serverkast_products_list
    ]
    # print(complete_serverkast_products_list)
    configured_serverkast_products_list = _apply_configuration_scheme(
        complete_serverkast_products_list, "Serverkast"
    )
    joined_list = (
        configured_topsystems_products_list + configured_serverkast_products_list
    )
    # print(joined_list)
    xml = dicttoxml(joined_list, custom_root="product_final_feed", attr_type=False)
    f = open(settings.LOCATION_OF_FINAL_FEED_FILE, "wb")
    f.write(xml)
    f.close()
    # selected_products_from_topsystems_products_list = Serverkast_Product.objects.filter(
    #     is_selected=True
    # ).values()
    # selected_products_from_topsystems_products_list = Serverkast_Product.objects.filter(
    #     name=True
    # ).values()
    # print(selected_products_from_topsystems_products_list)
    return context


def from_topsystems_feed(request):
    # feed = Feed.objects.get(shop_name=shop_name)
    # form = TopSystemsProductSelectForFinalFeedForm(request.POST)
    # form = SortingSelectForm()

    # if (feed.auto_add_new_products_cronjob_active):
    #     # print(request.POST)
    #     add_new_products(request, shop_name)
    """
    check
    products (in db)
    by
    form
    """

    # if form.is_valid():
    selected_products_from_database: QuerySet[Product] = Product.objects.filter(
        is_selected=True
    )
    selected_products_from_database_list: list = []
    for product in selected_products_from_database:
        selected_products_from_database_list.append(str(product))
    for form_product in request.POST:
        if " ––– " in form_product:
            product_name_of_form = form_product.split(" ––– ")[1]
            Product.objects.filter(name=product_name_of_form).update(is_selected=True)
    selected_products_from_form_list: list = []
    for value in request.POST:
        selected_products_from_form_list.append(str(value))
    for db_product in selected_products_from_database_list:
        # contnains substring?
        if any(db_product in s for s in selected_products_from_form_list):
            print("exist")
        else:
            print(db_product)
            print("exist not")
            Product.objects.filter(name=db_product).update(is_selected=False)

    # all_updated_products = TopSystemsProduct.objects.all()
    # template = get_template("master_list_page.html")
    # # has to be identical to field in product_feed_generator/forms/serverkast_product_select_for_final_feed_form.py
    # init = {
    #     "%s ––– %s" % (row.ean, row.name): row.is_selected
    #     for row in all_updated_products
    # }
    # form = TopSystemsProductSelectForFinalFeedForm(init)
    # context = {
    #     "feed": feed,
    #     "products": all_updated_products,
    #     "form": form,
    #     "message": "Products are added to Final Feed",
    # }
    # """
    # create
    # final
    # feed
    # from
    # checked
    # products (in db)
    # """
    # template = get_template("master_list_page.html")
    # selected_products_from_topsystems_products_list = TopSystemsProduct.objects.filter(
    #     is_selected=True
    # ).values()
    # complete_topsystems_products_list = [
    #     entry for entry in selected_products_from_topsystems_products_list
    # ]

    # configured_topsystems_products_list = _apply_configuration_scheme(
    #     complete_topsystems_products_list, "TopSystems"
    # )
    # # print(configured_topsystems_products_list)
    # selected_products_from_serverkast_products_list = Serverkast_Product.objects.filter(
    #     is_selected=True
    # ).values()
    # complete_serverkast_products_list = [
    #     entry for entry in selected_products_from_serverkast_products_list
    # ]
    # # print(complete_serverkast_products_list )
    # configured_serverkast_products_list = _apply_configuration_scheme(
    #     complete_serverkast_products_list, "Serverkast"
    # )
    # joined_list = (
    #     configured_topsystems_products_list + configured_serverkast_products_list
    # )
    # # print(joined_list)
    # xml = dicttoxml(joined_list, custom_root="product_final_feed", attr_type=False)
    # f = open(settings.LOCATION_OF_FINAL_FEED_FILE, "wb")
    # f.write(xml)
    # f.close()
    # return context
    return {}


# [0'additional_imagelinks,1"brand",2"categories",3"category",4"color",5"condition",6"delivery",7"description",8"ean",9"gender",10"id",11"image_link",12"is_in_stock",13"item_group_id",14"korting",15"link",16"manage_stock",17"material",18"max_price",19"min_price",20"min_sale_qty",21"price",22"prijs_amazon",23"product_type",24"qty_increments",25"shipping_weight",26"size",27"sku",28"special_price",29"special_price_from",30"special_price_to",31"status",32"stock",33"title",34"type",35"type_bootuitrusting",36"verzending",37"visibility"']

"""
writes
the
final feed
xml file
"""


def _add_products_to_final_feed(request):
    # if shop_name == "Serverkast":
    #     context = from_serverkast_feed(request, shop_name)

    context = from_topsystems_feed(request)
    return context
