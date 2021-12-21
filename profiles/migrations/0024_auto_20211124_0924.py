# Generated by Django 3.2.8 on 2021-11-24 06:24

from django.db import migrations, models
import profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0023_auto_20211123_1223'),
    ]

    operations = [
        migrations.RenameField(
            model_name='personal',
            old_name='location_county',
            new_name='county',
        ),
        migrations.RenameField(
            model_name='personal',
            old_name='location_address',
            new_name='location',
        ),
        migrations.RenameField(
            model_name='personal',
            old_name='location_location',
            new_name='town',
        ),
        migrations.RemoveField(
            model_name='personal',
            name='location_town',
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
