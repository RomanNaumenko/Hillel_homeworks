# Generated by Django 4.1.2 on 2022-10-26 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Coffee_night', '0002_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='approved_users',
        ),
        migrations.RemoveField(
            model_name='event',
            name='pending_users',
        ),
        migrations.AddField(
            model_name='event',
            name='event_users',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='route',
            name='stop_point',
            field=models.CharField(max_length=50),
        ),
    ]