from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.utils.http import is_safe_url

from .forms import LoginForm, RegisterForm, GuestForm
from .models import GuestEmail
# Create your views here.


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {"form": form}
    next_ = request.GET.get('next')
    next_post = request.POST.get('next') # to bedzie w url jako np /login/?next=/checkout/
    redirect_path = next_ or next_post #ten ktory nie jest Nonem
    if form.is_valid():
        user = authenticate(request, username=form.cleaned_data.get('username'),
                            password=form.cleaned_data.get('password'))
        if user is not None:
            # print("Logged in")
            login(request, user)
            # context["form"] = LoginForm()  # zeby wyczyscilo dane
            try: # nie wiem chyba zeby nie byc na guest jak sie logesz bo sie moze cos pomieszac
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        else:
            print("error")

    return render(request, "accounts/login_page.html", context)
    # return render(request, 'contact/view.html', {})
    # return HttpResponse("Dupa")


def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context = {"form": form}
    next_ = request.GET.get('next')
    next_post = request.POST.get('next') # to bedzie w url jako np /login/?next=/checkout/
    redirect_path = next_ or next_post #ten ktory nie jest Nonem
    if form.is_valid():
        email = form.cleaned_data.get('email')
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('register')

    return redirect("register")


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


    return render(request, "accounts/register_page.html", context)