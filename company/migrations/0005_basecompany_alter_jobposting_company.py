# Generated by Django 4.1.3 on 2023-01-11 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('company', '0004_remove_jobposting_company_name_jobposting_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                                           primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=200, null=True)),
                ('confirm_password', models.CharField(max_length=200,
                                                      null=True)),
                ('phone_number', models.CharField(max_length=255)),
                ('address', models.CharField(blank=True, default='',
                                             max_length=100, null=True)),
                ('legal_papers', models.FileField(upload_to='')),
                ('is_verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='jobposting',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.
                                    CASCADE, related_name='jobs',
                                    to='company.basecompany'),
        ),
    ]
