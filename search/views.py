from django.views.generic import ListView
from django.db.models import Q
from django.shortcuts import render
from products.models import Product

# Create your views here.
class SearchProductView(ListView):
    template_name = 'search/view.html' #jak zdefiniuje tak, to bedzie szukal w jednym i drugim

    def get_context_data(self, *args, **kwargs): #zawsze ta metoa jest w class based view
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q') #jak tego nie zrobimy to i tak mamy odwolanie do tego w template przez request.GET.q, automatycznie gety sa przekazywane do templata, ale tak wygondniej
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        print(request.GET)
        # w pzegladarce sie daje ?q=shirt i to jest wtedy w tym dict request.GET
        query = request.GET.get('q')
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.featured()

    '''
    __icontains = field contains this
    __iexact = field is exactly this
    in btoth cases capital letters does not matter
    '''