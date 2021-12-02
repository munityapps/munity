# Generated by Django 3.2.7 on 2021-10-24 03:07

from django.db import migrations, models
import munity.views


class Migration(migrations.Migration):

    dependencies = [
        ('generic_groups', '0006_alter_genericgroup_workspace'),
        ('users', '0012_remove_user_testt'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersViewSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generic_groups', models.ManyToManyField(blank=True, to='generic_groups.GenericGroup')),
            ],
            options={
                'abstract': False,
            },
            bases=(munity.views.MunityViewSet, models.Model),
        ),
    ]
