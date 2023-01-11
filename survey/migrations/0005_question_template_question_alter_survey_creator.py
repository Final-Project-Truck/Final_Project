# Generated by Django 4.1.3 on 2023-01-09 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('baseuser',
         '0004_remove_baseusers_password_baseusers_date_created_and_more'),
        ('survey', '0004_submission_submitter'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='template_question',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='survey',
            name='creator',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='baseuser.baseusers'),
        ),
    ]
