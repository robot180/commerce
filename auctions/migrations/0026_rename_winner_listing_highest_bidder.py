# Generated by Django 4.1.4 on 2023-02-12 04:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0025_listing_winner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='winner',
            new_name='highest_bidder',
        ),
    ]
