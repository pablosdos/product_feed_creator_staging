from django import forms
from django.db.models.query import QuerySet

from product_feed_generator.models import FeedConfiguration, Feed


class SortingSelectForm(forms.Form):
    CHOICES = (
        ("Sort by", "Sort by"),
        ("A - Z ↑", "A - Z ↑"),
        ("A - Z ↓", "A - Z ↓"),
        ("Price ↑", "Price ↑"),
        ("Price ↓", "Price ↓"),
    )
    FEEDS: list = [("All", "All")]
    # for feed in Feed.objects.all():
    #     FEEDS.append((feed.shop_name, feed.shop_name))
    feeds: list = [(feed, feed) for feed in Feed.objects.all()]
    FEEDS = FEEDS + feeds

    sorting_options = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.Select(
            attrs={
                "onchange": "form.submit();",
                "class": "form-select form-select-sm form-select-solid w-150px me-5",
            }
        ),
    )
    feed_source_selector = forms.ChoiceField(
        choices=FEEDS,
        widget=forms.Select(
            attrs={
                "onchange": "form.submit();",
                "class": "form-select form-select-solid",
            }
        ),
    )
    search_bar = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-solid ps-10",
                "placeholder": "Search",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for visible in self.visible_fields():
        #     visible.field.widget.attrs['class'] = 'form-select form-select-sm form-select-solid w-150px me-5'


# old feed_source_selector without dango form
# <select class="form-select form-select-solid"
#         data-control="select2"
#         data-placeholder="All"
#         data-hide-search="true"
#         onChange="form.submit();"
#         name="feed_source_selector">
#     <option value=""></option>
#     <option value="All">All</option>
#     {% for feed in feeds %}
#     <option value="{{feed}}">{{feed}}

#         {% endfor %}
# </select>
