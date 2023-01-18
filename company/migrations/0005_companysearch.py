# Generated by Django 4.1.3 on 2023-01-16 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_remove_jobposting_company_name_jobposting_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanySearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(null=True, verbose_name='date published')),
                ('author', models.CharField(max_length=200)),
                ('com_search', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companysearch', to='company.company')),
            ],
        ),
    ]
