from django.template.loader import get_template
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def product_selection_view(request):

    template = get_template("product_selection_page.html")

    context = {}
    return HttpResponse(template.render(context, request))
