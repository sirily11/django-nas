# Generated by Django 3.0 on 2020-04-13 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nas', '0020_auto_20200413_0317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musicmetadata',
            name='genre',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]