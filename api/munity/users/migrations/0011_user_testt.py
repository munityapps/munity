# Generated by Django 3.2.7 on 2021-10-19 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0002_alter_settings_workspace'),
        ('users', '0010_alter_user_workspace'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='testt',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='settings.settings'),
        ),
    ]