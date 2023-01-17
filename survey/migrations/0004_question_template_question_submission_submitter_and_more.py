# Generated by Django 4.1.3 on 2023-01-17 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('baseuser', '0002_companyprofile_userprofile_remove_baseusers_password_and_more'),
        ('survey', '0003_alter_submission_survey_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='template_question',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='submission',
            name='submitter',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='baseuser.baseusers'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='survey',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='baseuser.baseusers'),
        ),
    ]
