# Generated by Django 4.1.3 on 2023-05-17 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0008_alter_establishments_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='establishments',
            name='logo',
            field=models.ImageField(blank=True, default='logo.jpg', null=True, upload_to=''),
        ),
    ]