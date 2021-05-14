# Generated by Django 3.2 on 2021-05-10 13:50

from django.db import migrations, models
import mysite.models.profile_models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='', upload_to=mysite.models.profile_models.upload_image_to),
        ),
    ]