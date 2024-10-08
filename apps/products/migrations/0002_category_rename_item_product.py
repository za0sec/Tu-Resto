# Generated by Django 5.1 on 2024-09-09 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='categories')),
            ],
        ),
        migrations.RenameModel(
            old_name='Item',
            new_name='Product',
        ),
    ]
