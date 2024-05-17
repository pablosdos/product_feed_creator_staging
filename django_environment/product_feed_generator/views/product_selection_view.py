from django.template.loader import get_template
from django.http import HttpResponse
from django.db.models.query import QuerySet
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from product_feed_generator.models import Product, Feed
from product_feed_generator.forms import (
    ProductSelectForFinalFeedForm,
    SortingSelectForm,
)


@login_required
def product_selection_view(request):

    template = get_template("product_selection_page.html")
    if request.method == "GET":
        selected_products_from_database: QuerySet[Product] = Product.objects.filter(
            is_selected=True
        )
        paginator = Paginator(selected_products_from_database, 50)
        page_number = request.GET.get("page")
        paginator_control_with_products_queryset = paginator.get_page(page_number)
        paginated_form = ProductSelectForFinalFeedForm(
            paginator_control_with_products_queryset
        )
    feeds = Feed.objects.all()
    if not "sort_type" in locals():
        sort_type: str = "Sort by"
    if not "sorting_option_form" in locals():
        sorting_option_form = SortingSelectForm()
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
    return HttpResponse(template.render(context, request))
