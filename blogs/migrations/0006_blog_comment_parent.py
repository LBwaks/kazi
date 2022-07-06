# Generated by Django 3.2.8 on 2022-02-28 03:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0005_blog_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog_comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='blogs.blog_comment'),
        ),
    ]