# Generated by Django 3.2.8 on 2021-11-24 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_rename_contant_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='description',
            new_name='message',
        ),
    ]
