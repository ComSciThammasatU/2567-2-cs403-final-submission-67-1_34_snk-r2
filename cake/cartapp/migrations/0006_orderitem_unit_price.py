# Generated by Django 5.1.6 on 2025-04-17 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartapp', '0005_order_cancel_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
