# Generated by Django 3.2.7 on 2021-12-02 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0009_alter_workspace_slug'),
        ('records', '0008_remove_record_model_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='record',
            options={'get_latest_by': 'modified'},
        ),
        migrations.RenameField(
            model_name='record',
            old_name='next_value',
            new_name='diff_value',
        ),
        migrations.AddField(
            model_name='record',
            name='action',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='record',
            name='workspace',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='workspaces.workspace'),
        ),
    ]
