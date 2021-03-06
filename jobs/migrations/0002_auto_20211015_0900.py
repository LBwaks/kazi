# Generated by Django 3.2.8 on 2021-10-15 06:00

import autoslug.fields
import ckeditor.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=ckeditor.fields.RichTextField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=django.utils.timezone.now, editable=False, populate_from='name', unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job',
            name='description',
            field=ckeditor.fields.RichTextField(default='hey'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job',
            name='image',
            field=models.ImageField(blank=True, default='job_images/jobs.jpg', null=True, upload_to='jobs/job_images/'),
        ),
        migrations.AddField(
            model_name='job',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=4, editable=False, populate_from='title', unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='jobs/job_videos/'),
        ),
        migrations.AddField(
            model_name='tag',
            name='description',
            field=ckeditor.fields.RichTextField(default=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=3, editable=False, populate_from='name', unique=True),
            preserve_default=False,
        ),
    ]
