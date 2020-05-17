from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from .forms import ContactForm


def home_page(request):
    context = {"title": "Home page"}
    if request.user.is_authenticated:
        context["premium_content"] = "Premium for being logged in" #jeden sposob, mozna tez w templatce
    return render(request, 'home_page.html', context)


def about_page(request):
    context = {"title": "About page"}
    return render(request, 'home_page.html', context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {"title": "Contact page",
               "form": contact_form}
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    # if request.method == "POST":
    #     print(request.POST.get('fullname')) #fullname to klucz w dict zwracanym przez posta
    #     print(request.POST.get('email'))
    #     print(request.POST.get('content'))
    return render(request, 'contact/view.html', context)



