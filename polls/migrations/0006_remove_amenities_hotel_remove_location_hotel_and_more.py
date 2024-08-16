# Generated by Django 5.1 on 2024-08-16 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_remove_hotelinformation_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='amenities',
            name='hotel',
        ),
        migrations.RemoveField(
            model_name='location',
            name='hotel',
        ),
        migrations.AddField(
            model_name='amenities',
            name='hotels',
            field=models.ManyToManyField(related_name='amenities', to='polls.hotelinformation'),
        ),
        migrations.AddField(
            model_name='location',
            name='hotels',
            field=models.ManyToManyField(related_name='locations', to='polls.hotelinformation'),
        ),
    ]
