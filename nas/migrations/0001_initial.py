# Generated by Django 3.0.3 on 2020-04-21 20:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import nas.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BookCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_type', models.CharField(choices=[('Image', 'image'), ('Text', 'txt'), ('File', 'file')], default='file', max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('size', models.FloatField(blank=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(max_length=1000000, upload_to=nas.models.user_directory_path)),
                ('transcode_filepath', models.FileField(blank=True, null=True, upload_to='')),
                ('cover', models.FileField(blank=True, null=True, upload_to='')),
                ('has_uploaded_to_cloud', models.BooleanField(blank=True, default=False, null=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(blank=True, max_length=1024, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('sender', models.CharField(default='system', max_length=128)),
                ('log_type', models.CharField(choices=[('CREATED', 'created'), ('DELETED', 'deleted'), ('UPDATED', 'updated'), ('LOG', 'log')], max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='MusicMetaData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=1024, null=True)),
                ('album', models.CharField(blank=True, max_length=1024, null=True)),
                ('artist', models.TextField(blank=True, max_length=1024, null=True)),
                ('album_artist', models.TextField(blank=True, max_length=1024, null=True)),
                ('year', models.CharField(default='2020', max_length=128)),
                ('track', models.IntegerField(default=0)),
                ('genre', models.CharField(blank=True, max_length=128, null=True)),
                ('picture', models.FileField(blank=True, null=True, upload_to='music-cover/%Y/%m/%d')),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('like', models.BooleanField(default=False)),
                ('file', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='metadata', to='nas.File')),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(default='', max_length=128)),
                ('description', models.TextField(blank=True, null=True)),
                ('size', models.FloatField(blank=True, default=0, null=True)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='folders', to='nas.Folder')),
            ],
        ),
        migrations.AddField(
            model_name='file',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='nas.Folder'),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(default='', max_length=128)),
                ('description', models.TextField(blank=True, null=True)),
                ('size', models.FloatField(blank=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('show_in_folder', models.BooleanField(default=True)),
                ('collection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='books', to='nas.BookCollection')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='nas.Folder')),
            ],
        ),
    ]
