# Generated by Django 3.0 on 2020-04-13 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nas', '0023_auto_20200413_0657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musicmetadata',
            name='year',
            field=models.CharField(default='2020', max_length=128),
        ),
    ]