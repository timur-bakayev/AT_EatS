# Generated by Django 4.1.3 on 2023-05-16 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0006_foodcategory_remove_establishments_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='establishments',
            name='photo',
            field=models.ImageField(blank=True, default='images.jpg', null=True, upload_to=''),
        ),
    ]
