from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from datetime import date
from product_feed_generator.forms import FeedForm
from product_feed_generator.models import FeedConfiguration, Feed

@login_required
def new_feed_meta_data_view(request):
    request_post = request.POST
    context = {}
    form = FeedForm(request.POST or None, request.FILES or None)

    if "nextBtn" in request_post:

        if form.is_valid():
            form_ = form.save(commit=False)
            shop_name: str =form.cleaned_data["shop_name"] 
            form_.available_fields = "[" + form.cleaned_data["available_fields"] + "]"
            form_.products_update_cronjob_active = False
            form_.auto_add_new_products_cronjob_active = False
            form_.products_last_updated = date.today()
            form.save()            
            return redirect("input_feed_mapping_page", shop_name=shop_name)
    
    context["form"] = form
    return render(request, "new_feed_meta_data_page.html", context)
