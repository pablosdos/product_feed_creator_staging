from django.template.loader import get_template
from django.http import HttpResponse
from product_feed_generator.models import Feed, Serverkast_Product
from django.contrib.auth.decorators import login_required

@login_required
def feed_selection_view(request):
    feeds = Feed.objects.all()
    context = {
        "feeds": feeds,
    }
    template = get_template("feed_selection_page.html")
    return HttpResponse(template.render(context, request))
