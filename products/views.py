from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from django.http import Http404


from .models import Product
# Create your views here.

# w glownym programie mielismy function based view co jest niby latwe, tutaj jakis class based view trudniejszy

class ProductListView(ListView):
    # queryset = Product.objects.all()
    # "products/product_list.html" taki html dobierze jako default, ale mozna zmieniac
    template_name = 'products/list.html' #jak zdefiniuje tak, to bedzie szukal w jednym i drugim

    #to wykorzystaismy tylko zeby wyprintowac caly context jaki mamy, ale ta metoda juz jest zdefiniowana i dziedziczona przez nas w ListView
    # def get_context_data(self, *args, **kwargs): #zawsze ta metoa jest w class based view
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

    def get_queryset(self, *args, **kwargs): # zastepujemy ten queryset u gory, chyba zeby mozna bylo go filtrowac, ale nie jestm pewny do konca czemu to dodalismy
        request = self.request
        return Product.objects.all()


def product_list_view(request): #to sa niby dwa sposoby podobne na zrobienie tego samego, ale nie wiem czy tak clkowicie tego samego
    queryset = Product.objects.all()
    context = {
        'object_list': queryset #klasyczny sposob i w htmlu {{qs}} i wyswietla
        #po zmienia qs na object list mamy tak samo jak u gory, ta sama zmienna zawiera context object list
    }
    return render(request, 'products/list.html', context)

class ProductDetailView(DetailView):
    # queryset = Product.objects.all()
    template_name = 'products/detail.html'

    # def get_context_data(self, *args, **kwargs): #zawsze ta metoa jest w class based view
    #     context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context #{'object': <Product: Hat>, 'product': <Product: Hat>, 'view': <products.views.ProductDetailView object at 0x0000028981441C50>}

    def get_object(self, *args, **kwargs): #to robi to samo co co w tym detail view, nie do konca wiem czemu bo to chyba aytomatycznie sie dzialo z tym odkomentowanym querysetem u gory
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Product doesn't exist")
        return instance




def product_detail_view(request, pk=None, *args, **kwargs): #bez tego pk = None wywala blad ze name pk is not defined
    # print(args)
    # print(kwargs) ## to printuje slownik {'pk: cos tam} czyli primary key, index danego objektu
    # instance = Product.objects.get(pk=pk)
    # instance = get_object_or_404(Product, pk=pk) #w tym detailview klasa automatycznie sie to dzieje nie trzeba dodawac erroru 404 tylko wywoluje sie sam
    #jak samemu obsluzyc cos takiego jak ten error 404 przyklad pokazany
    # try:
    #     instance = Product.objects.get(id=pk)
    # except Product.DoesNotExist:
    #     print('No product here')
    #     raise Http404("Product doesn't exist") # ta wersja u gory z get object or 404 diala tak samo tylko inna informacje wystawia
    # except:
    #     print('Huh?')


    # #ponizej jeszcze kolejny sposob na zrobienie tego samego
    # qs = Product.objects.filter(id=pk)
    # if qs.exists() and qs.count() == 1:
    #     instance = qs.first()
    # else:
    #     raise Http404("Product doesn't exist")


    # ostateczna wersja, wykorzystujaca ta metode zaimplementowana po stronie modelu
    instance = Product.objects.get_by_id(pk)  # to metoda ktora stworzylismy po stronie menagera modelu
    if instance is None:
        raise Http404("Product doesn't exist")

    context = {
        'object': instance #object dlatego ze context tam u gory dla klasy sie nazywa object tez
    }
    return render(request, 'products/detail.html', context)


class ProductFeaturedListView(ListView):
    template_name = "products/list.html"

    def get_queryset(self, *args, **kwargs): #tej metody  nietrzeba tu tworzyc, wystarczy u gory querystet=Product.objects.featured()
        request = self.request
        return Product.objects.featured() #featuredstworzona przez nas w models


class ProductFeaturedDetailView(DetailView):
    template_name = "products/featured-detail.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.featured() # on w tym class based automatycznie srawdze najpierw wszystkie featured i potem zwraca ten ktory pasuje do primary key podanego w url

class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = 'products/detail.html'

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        # instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404('Not Found')
        except Product.MultipleObjectsReturned: #jak kilka ma ten sam slug
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Unknown error")

        return instance
