# Generated by Django 4.1.3 on 2022-12-08 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('survey', '0002_alter_answerchoice_submission_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='survey',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='survey_submission', to='survey.survey'),
        ),
        migrations.AlterField(
            model_name='surveyquestion',
            name='question',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='survey_question', to='survey.question'),
        ),
    ]
