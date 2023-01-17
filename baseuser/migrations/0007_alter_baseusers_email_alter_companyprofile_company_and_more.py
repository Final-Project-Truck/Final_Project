# Generated by Django 4.1.3 on 2023-01-17 22:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_remove_jobposting_company_name_jobposting_company'),
        ('baseuser', '0006_rename_type_companyprofile_organization_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseusers',
            name='email',
            field=models.EmailField(max_length=200, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='companyprofile',
            name='company',
            field=models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='company_user', to='company.company'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='past_companies',
            field=models.ManyToManyField(blank=True, related_name='past_companies', to='company.company'),
        ),
    ]
