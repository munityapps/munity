# Generated by Django 3.2.7 on 2021-12-15 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_file_generic_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='disabled',
            field=models.BooleanField(default=False),
        ),
    ]
