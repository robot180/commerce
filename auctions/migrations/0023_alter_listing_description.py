# Generated by Django 4.1.4 on 2023-02-10 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0022_alter_listing_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.TextField(blank='True', default='', max_length=500),
            preserve_default=False,
        ),
    ]