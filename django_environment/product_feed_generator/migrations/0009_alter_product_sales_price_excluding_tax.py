# Generated by Django 5.0.2 on 2024-06-07 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "product_feed_generator",
            "0008_feed_is_new_feed_alter_feed_input_url_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="sales_price_excluding_tax",
            field=models.FloatField(max_length=65535),
        ),
    ]
