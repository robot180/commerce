# Generated by Django 4.1.4 on 2023-02-10 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0021_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.TextField(blank='True', max_length=500, null='False'),
        ),
    ]