# Generated by Django 3.2.7 on 2021-10-17 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0002_auto_20211017_2017'),
        ('generic_groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericgroup',
            name='related_workspace',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='workspaces.workspace'),
        ),
    ]