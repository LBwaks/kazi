# Generated by Django 3.2.8 on 2021-12-12 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0012_alter_tag_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='image',
            field=models.ImageField(blank=True, default='jobs/job_images/jobs.jpg', null=True, upload_to='jobs/job_images/'),
        ),
    ]
