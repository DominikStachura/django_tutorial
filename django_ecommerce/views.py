from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from .forms import ContactForm, LoginForm, RegisterForm


def home_page(request):
    r
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


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {"form": form}
    # print(request.user.is_authenticated)
    if form.is_valid():
        user = authenticate(request, username=form.cleaned_data.get('username'),
                            password=form.cleaned_data.get('password'))
        if user is not None:
            print("Logged in")
            login(request, user)
            context["form"] = LoginForm()  # zeby wyczyscilo dane
            redirect("/")
        else:
            print("error")

    return render(request, "auth/login_page.html", context)
    # return render(request, 'contact/view.html', {})
    # return HttpResponse("Dupa")


User = get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {"form": form}
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        new_user = User.objects.create_user(username, email, password) #mozna to chyba wszystko latwiej z wykorzystaniem UserCreationForm z django
        print(new_user)


    return render(request, "auth/register_page.html", context)
