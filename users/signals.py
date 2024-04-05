from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def verify_user_profile_is_created(instance: User, created: bool, **kwargs):
    if created:
        instance.profile = Profile.objects.create(user=instance)
        instance.save()
