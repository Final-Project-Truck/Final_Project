# Generated by Django 4.1.3 on 2022-11-21 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answerchoice',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choice_submission', to='survey.submission'),
        ),
        migrations.AlterField(
            model_name='answertext',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_submission', to='survey.submission'),
        ),
    ]
