# Generated by Django 3.2 on 2024-10-16 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_gallery_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='description',
            field=models.TextField(default='Author description'),
        ),
    ]
