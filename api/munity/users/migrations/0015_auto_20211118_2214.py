# Generated by Django 3.2.7 on 2021-11-18 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20211118_2146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='roles',
        ),
        migrations.AddField(
            model_name='user',
            name='workspace_roles',
            field=models.ManyToManyField(related_name='workspace_roles', to='users.UserRoleWorkspace'),
        ),
    ]
