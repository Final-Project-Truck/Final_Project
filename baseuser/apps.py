from django.apps import AppConfig


class BaseuserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'baseuser'

    # def ready(self):
    #     import baseuser.signals
