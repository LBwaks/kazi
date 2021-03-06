# Generated by Django 3.2.8 on 2021-11-24 06:32

from django.db import migrations, models
import profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0024_auto_20211124_0924'),
    ]

    operations = [
        migrations.RenameField(
            model_name='personal',
            old_name='town',
            new_name='address',
        ),
        migrations.AlterField(
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
