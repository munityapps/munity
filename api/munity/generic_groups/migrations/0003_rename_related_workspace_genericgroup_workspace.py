# Generated by Django 3.2.7 on 2021-10-17 20:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('generic_groups', '0002_genericgroup_related_workspace'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genericgroup',
            old_name='related_workspace',
            new_name='workspace',
        ),
    ]
