# Generated by Django 3.2.7 on 2021-10-19 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0008_alter_workspace_db_connection'),
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='workspace',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='workspaces.workspace'),
        ),
    ]
