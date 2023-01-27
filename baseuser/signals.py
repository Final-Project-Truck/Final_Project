# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from .models import BaseUsers, UserProfile, CompanyProfile
#
# #todo transaction
# @receiver(post_save, sender=BaseUsers)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         if instance.user_type == 'per':
#             UserProfile.objects.create(base_user=instance)
#         elif instance.user_type == 'com':
#             CompanyProfile.objects.create(base_user=instance)
#
#
# @receiver(post_save, sender=User)
# def create_baseuser(sender, instance, created, **kwargs):
#     if created:
#         BaseUsers.objects.create(django_user=instance)
#
