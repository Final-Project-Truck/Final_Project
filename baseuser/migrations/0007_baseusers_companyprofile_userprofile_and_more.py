# Generated by Django 4.1.3 on 2023-01-17 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseuser', '0006_rename_baseusers_baseuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200, null=True)),
                ('password1', models.CharField(max_length=200, null=True)),
                ('password2', models.CharField(max_length=200, null=True)),
                ('email', models.EmailField(max_length=200, null=True, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('user_type', models.CharField(choices=[('per', 'Person'), ('com', 'Company')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('website', models.URLField()),
                ('number_of_employees', models.IntegerField()),
                ('organization_type', models.CharField(choices=[('pub', 'Public'), ('pri', 'Private'), ('sel', 'Self-Employed'), ('oth', 'Other')], max_length=3)),
                ('revenue', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(default='tinyurl.com/2a382vsm', upload_to='profile_images')),
                ('about', models.TextField(max_length=250, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='baseuser',
            name='django_user',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='base_user',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='current_company',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='past_companies',
        ),
    ]
