# Generated by Django 4.1.2 on 2023-01-31 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_listing_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(blank=True, default=None, upload_to='images/'),
        ),
    ]
