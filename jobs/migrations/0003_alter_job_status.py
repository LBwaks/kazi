# Generated by Django 3.2.8 on 2021-10-17 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_auto_20211015_0900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.CharField(blank=True, default='waiting', max_length=250, null=True),
        ),
    ]