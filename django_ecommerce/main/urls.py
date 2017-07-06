from django.conf.urls import url
from . import json_views
urlpatterns = [
    url(r'^status_reports/$',json_views.status_collection),
    url(r'^status_reports/(?P<id>[0-9]+)$', json_views.status_member)
]
