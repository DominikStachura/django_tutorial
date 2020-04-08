from django.conf.urls import url
from django.urls import path

from .views import product_list_view, ProductListView, product_detail_view, ProductDetailView, \
    ProductFeaturedDetailView, ProductFeaturedListView, ProductDetailSlugView

# from .views import home_page, about_page, contact_page, login_page, register_page
app_name = 'products'
urlpatterns = [
    #wszystkie sa zakomentowane bo to bardziej bylo tak zeby sie pouczyc tego, zostaja dwa ktore beda fakycznie potrzebne
    # url(r'^products/$', ProductListView.as_view()), #as_view bo jest to klasa, a chcey callable item
    # url(r'^products-fbv/$', product_list_view), #fbv od function based view
    # #url(r'^products/(?P<pk>\d+)/$', ProductDetailView.as_view()), #common regular expressions for django urls - mozna doczytac
    #                                                    #http://127.0.0.1:8000/admin/products/product/1/change/
    #                                                    #takie cos widac w django admin i ta 1 to jest chyba to wlasnie id danego produktu
    # url(r'^products/(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view()),    # obsluga slugow w url, regex wziety ze strony tej z tutiralem do regexoq url django, ten u gory zakomentowany bo chcemy przez slug
    # url(r'^products-fbv/(?P<pk>\d+)/$', product_detail_view),
    # url(r'^featured/$', ProductFeaturedListView.as_view()),
    # url(r'^featured/(?P<pk>\d+)/$', ProductFeaturedDetailView.as_view())
    url(r'^$', ProductListView.as_view(), name='list'), #usuniete jest /products, bo w glownym urls to jest,a te dwa tu to to co po products/
    # url(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail')
    path('<slug:slug>/', ProductDetailSlugView.as_view(), name='detail')  # to znalazlem na internecie, chyba dziala tak samo a prosciej
]

