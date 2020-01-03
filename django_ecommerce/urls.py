"""django_ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from products.views import product_list_view, ProductListView, product_detail_view, ProductDetailView, \
    ProductFeaturedDetailView, ProductFeaturedListView

from .views import home_page, about_page, contact_page, login_page, register_page

urlpatterns = [
    url(r'^$', home_page),
    url(r'^about/$', about_page),
    url(r'^contact/$', contact_page),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', login_page),
    url(r'^register/$', register_page),
    url(r'^products/$', ProductListView.as_view()), #as_view bo jest to klasa, a chcey callable item
    url(r'^products-fbv/$', product_list_view), #fbv od function based view
    url(r'^products/(?P<pk>\d+)/$', ProductDetailView.as_view()), #common regular expressions for django urls - mozna doczytac
                                                       #http://127.0.0.1:8000/admin/products/product/1/change/
                                                       #takie cos widac w django admin i ta 1 to jest chyba to wlasnie id danego produktu
    url(r'^products-fbv/(?P<pk>\d+)/$', product_detail_view),
    url(r'^featured/$', ProductFeaturedListView.as_view()),
    url(r'^featured/(?P<pk>\d+)/$', ProductFeaturedDetailView.as_view())
]

if settings.DEBUG:  # dzieki temu jak mamy w settingsach debug na false, czyli wypuszczamy nasza aplikacje na zewnetrzny serwer, do produkcji, to pliki statyczne nie sa obslugiwane, czyli tak jak ma byc
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
