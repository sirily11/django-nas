# Generated by Django 3.0 on 2019-12-14 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nas', '0012_auto_20191214_0403'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='cover',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
