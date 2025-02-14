# signals.py
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Customer
from django.contrib.auth import get_user_model
from django.conf import settings

@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

@receiver(post_save, sender=User)   
def save_customer(sender, instance, **kwargs):
    instance.customer.save()

post_save.connect(save_customer,sender=settings.AUTH_USER_MODEL)