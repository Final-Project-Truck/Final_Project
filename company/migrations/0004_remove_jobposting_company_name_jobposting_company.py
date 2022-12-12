# Generated by Django 4.1.3 on 2022-12-08 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_jobposting_delete_jobdescription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobposting',
            name='company_name',
        ),
        migrations.AddField(
            model_name='jobposting',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='company.company'),
            preserve_default=False,
        ),
    ]
