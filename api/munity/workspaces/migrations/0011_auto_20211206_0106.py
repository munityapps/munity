# Generated by Django 3.2.7 on 2021-12-06 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0010_alter_workspace_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='workspace',
            name='name',
            field=models.CharField(blank=True, max_length=258, null=True),
        ),
        migrations.AlterField(
            model_name='workspace',
            name='db_connection',
            field=models.CharField(default='', max_length=100),
        ),
    ]
