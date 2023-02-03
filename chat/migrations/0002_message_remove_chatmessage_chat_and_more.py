# Generated by Django 4.1.3 on 2023-01-24 21:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id',
                 models.BigAutoField(auto_created=True, primary_key=True,
                                     serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=1200)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('receiver',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='receiver',
                                   to=settings.AUTH_USER_MODEL)),
                ('sender',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   related_name='sender',
                                   to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('timestamp',),
            },
        ),
        migrations.RemoveField(
            model_name='chatmessage',
            name='chat',
        ),
        migrations.RemoveField(
            model_name='chatmessage',
            name='sender',
        ),
        migrations.RemoveField(
            model_name='chatparticipant',
            name='chat',
        ),
        migrations.RemoveField(
            model_name='chatparticipant',
            name='user',
        ),
        migrations.DeleteModel(
            name='Chat',
        ),
        migrations.DeleteModel(
            name='ChatMessage',
        ),
        migrations.DeleteModel(
            name='ChatParticipant',
        ),
    ]
