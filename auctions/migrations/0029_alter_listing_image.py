# Generated by Django 4.1.4 on 2023-02-23 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0028_alter_listing_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(blank=True, default='static/auctions/No-Image-Placeholder.svg.png', upload_to='images/'),
        ),
    ]
