# Generated by Django 5.1 on 2024-09-09 02:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_categoryextra_product_category_product_discount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productextra',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.categoryextra'),
        ),
    ]
