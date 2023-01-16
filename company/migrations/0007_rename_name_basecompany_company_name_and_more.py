# Generated by Django 4.1.3 on 2023-01-12 11:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company',
         '0006_remove_basecompany_address_remove_basecompany_email_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basecompany',
            old_name='name',
            new_name='company_name',
        ),
        migrations.AddField(
            model_name='basecompany',
            name='email',
            field=models.EmailField(max_length=200, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='basecompany',
            name='user',
            field=models.OneToOneField(default=1,
                                       on_delete=django.db.models.
                                       deletion.CASCADE,
                                       related_name='BaseCompany',
                                       to=settings.AUTH_USER_MODEL),
        ),
    ]
