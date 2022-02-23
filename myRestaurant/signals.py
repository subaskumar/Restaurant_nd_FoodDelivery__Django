from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import UserAccount

## receiver method only once will called when action is performed on sender Model.
@receiver(post_save, sender = UserAccount)
def update_User_signal(sender, instance, created, **kwargs):
    if created:
        instance.is_active = False
        instance.save()
        print("signal is called")
