# Generated by Django 3.2 on 2021-06-01 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invites', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invite',
            name='invite_estimate_timestamp_invalid',
            field=models.PositiveIntegerField(default=None),
            preserve_default=False,
        ),
    ]