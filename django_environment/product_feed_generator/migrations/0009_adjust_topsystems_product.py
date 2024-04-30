# Generated by Django 4.2.6 on 2023-11-06 15:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product_feed_generator", "0008_adjust_topsystems_product"),
    ]

    operations = [
        migrations.AlterField(
            model_name="topsystemsproduct",
            name="gross_price",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=9,
                verbose_name="Gross Price – calculated from original Price",
            ),
        ),
    ]
