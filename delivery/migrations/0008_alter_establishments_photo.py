# Generated by Django 4.1.3 on 2023-05-16 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0007_establishments_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='establishments',
            name='photo',
            field=models.ImageField(blank=True, default='images.jpeg', null=True, upload_to=''),
        ),
    ]