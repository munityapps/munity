# Generated by Django 3.2.7 on 2021-10-17 21:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0006_auto_20211017_2105'),
        ('generic_groups', '0004_remove_genericgroup_workspace'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericgroup',
            name='workspace',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='workspaces.workspace'),
        ),
    ]
