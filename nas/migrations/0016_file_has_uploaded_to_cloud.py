# Generated by Django 3.0 on 2020-01-31 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nas', '0015_auto_20191216_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='has_uploaded_to_cloud',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
