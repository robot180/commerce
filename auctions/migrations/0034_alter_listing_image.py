# Generated by Django 4.1.4 on 2023-02-23 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0033_alter_listing_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(blank=True, default='/images/No-Image-Placeholder.svg.png', null='False', upload_to='images/'),
        ),
    ]
