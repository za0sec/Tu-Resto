# Generated by Django 5.1 on 2024-09-09 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_remove_takeawayorder_cashier_and_more'),
        ('products', '0007_category_identifier_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='extras',
            field=models.ManyToManyField(blank=True, null=True, to='products.productextra'),
        ),
    ]
