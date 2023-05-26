# Generated by Django 4.1.3 on 2023-05-10 12:41

from django.db import migrations, models
import django.db.models.deletion
import geolocation_fields.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0004_category_establishments_order_profile_orderlist_menu_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geo', geolocation_fields.models.fields.PointField()),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='delivery.location'),
        ),
        migrations.AddField(
            model_name='establishments',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='delivery.location'),
        ),
    ]
