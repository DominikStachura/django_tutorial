from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

from accounts.models import GuestEmail
User = settings.AUTH_USER_MODEL


class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None
        if user.is_authenticated:
            obj, created = self.model.objects.get_or_create(user=user, email=user.email) # jaka jest zalogowany to jego billing profilembierzemy

        elif guest_email_id is not None:
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(email=guest_email_obj.email)

        else:
            pass
        return obj, created


# ogolnie ma byc tak ze uzytkownik bez konta np
# abc@costam.com -> 1000 billing profili, ile zakupow tyle ich ma
# ale zarejestrowany user abc@costam.com -> 1 tylko moze miec billing
class BillingProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE) # czyli user jest unique nie mozna tego samego biling z tym samym userem powiazac
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.email

# def user_created_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         print('send to stripe/braintree')
#         instance.customer_id = newID
#         instance.save()


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email: #czyli jak tworzymy nowego usera to na poczatku robimy mu billingprofile
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_created_receiver, sender=User)