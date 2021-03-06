# Generated by Django 3.2.8 on 2021-11-18 06:22

from django.db import migrations, models
import profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0016_auto_20211110_1328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personal',
            name='certificates',
        ),
        migrations.RemoveField(
            model_name='personal',
            name='good_conduct',
        ),
        migrations.AddField(
            model_name='personal',
            name='cv',
            field=models.FileField(blank=True, null=True, upload_to=profiles.models.user_documents_path),
        ),
        migrations.AlterField(
            model_name='personal',
            name='id_back',
            field=models.ImageField(blank=True, null=True, upload_to=profiles.models.user_id_path),
        ),
        migrations.AlterField(
            model_name='personal',
            name='id_front',
            field=models.ImageField(blank=True, null=True, upload_to=profiles.models.user_id_path),
        ),
    ]
