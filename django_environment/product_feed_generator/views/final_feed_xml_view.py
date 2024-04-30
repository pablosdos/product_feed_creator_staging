# from django.template.loader import get_template
# from django.http import HttpResponse
# import os
# from django.shortcuts import render


# def final_feed_xml_view(request):
#     if os.path.isfile("final-feed-file.xml"):
#         return render(request, 'final-feed-file.xml', content_type='text/xml')
#     else:
#         context = {
#             "message": "No Final Feed File! Please generate one."
#         }
#         template = get_template("final_feed_page.html")
#         return HttpResponse(template.render(context, request))
