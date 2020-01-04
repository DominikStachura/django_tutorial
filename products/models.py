from django.db import models
from django.db.models.signals import pre_save, post_save
import random
import os
from .utils import unique_slug_generator

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 947123878)
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'
    return f'products/{new_filename}/{final_filename}' #generalnie chodzi chyba o to, ze jak wgrywamy jakis plik, to jego nazwa moze zawierac spacja albo inne dziwne znaki
                                                        #i to ma nas uchronic przed problemami zwiazanymi z tym


# Create your models here.
class ProductQuerySet(models.query.QuerySet): # to sa wszystkie operacje wywolywane na querysecie, czyli na tym co zwraca get_queryset
    def active(self):
        return self.filter(active=True) #teraz objects.all() bedzie zwracac tylko active

    def featured(self):
        return self.filter(featured=True, active=True)

class ProductManager(models.Manager):
    def get_queryset(self): #przeciazam get_queryset dla Product, tym custom querysetems tworzonym u gory
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active() #przeciazam metoda all tak, zby zwracala query tylko z obiektami ktora sa aktualanie active

    def featured(self): #to nie jest to samo featured co u gory, ten dziala na Product.objects bo to jest model menager, ten u gory dziala na queryset czyli na Product,objects.all() np, czyli jakby na wynik sqlowgo query wywolanego na tablicy
        return self.get_queryset().featured() #dodalismy pole featured i tworzymy metode do pobieranie wszystkich z featured = true

    def get_by_id(self, id):
        QS = self.get_queryset().filter(id=id)  #get_queryset() to tak jak Product.objects
        if QS.count() == 1:
            return QS.first()
        return None


class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True) # unique zeby kazdy produkt mial inny slug
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10,
                                default=39.99)  # default trzeba zeby sie migracje robily do istniejacych juz obiektow tej tablicy ktore nie maja nowoutworzonej kolumny
    image = models.ImageField(upload_to=upload_image_path, null=True,
                             blank=True)  # ten folder media/ co w settingsach ustawialem do ,statics file
                                            #upload po stronie admina dodaje od razu do tamtego folderu obrazek

                                            #do uploadowanie wiekszych plikow jest jakas inna technika amazon cos tam, to tylko na male
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    objects = ProductManager() # model.objects to jest zawsze menager tego modelu. To co tutaj robimy to nie nadpisanie go, a rozszerzenie, dodaje nowa metode do istniejacego menagera czyli do .objects

    def get_absolute_url(self):
        return f"/products/{self.slug}/"

    def __str__(self):  # zeby wyswietlalo ladnie a nie Product Object 1..
        return self.title

def product_pre_save_receiver(sender, instance, *args, **kwargs): #robimy to aby zapobiec temu ze bedzie pusty slug, jak zapiszemy z pustym to sie doda randomowy
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product) #zanim sie zapisze obiekt, to wywoluje cos takiego chyba