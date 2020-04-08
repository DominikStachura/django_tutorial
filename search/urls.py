from django.conf.urls import url
from django.urls import path

from .views import SearchProductView

app_name = 'search'
urlpatterns = [
    url(r'^$', SearchProductView.as_view(), name='query'),
    ]