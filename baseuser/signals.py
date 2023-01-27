from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from baseuser.models import BaseUsers, UserProfile


# @receiver(post_save, sender=BaseUsers)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and instance.user_type == 'per':
#         UserProfile.objects.create(base_user=instance)
#
#
# @receiver(post_save, sender=BaseUsers)
# def save_profile(sender, instance, **kwargs):
#     if instance.pk and instance.user_type == 'com':
#         instance.profile.save()

# @receiver(post_save, sender=User)
# def create_baseuer(sender, instance, created, **kwargs):
#     if created:
#         BaseUsers.objects.create(base_user_id=instance.id)
#
#
# @receiver(post_save, sender=User)
# def save_baseuser(sender, instance, **kwargs):
#     instance.baseuser.save()
