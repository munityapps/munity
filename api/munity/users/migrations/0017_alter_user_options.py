# Generated by Django 3.2.7 on 2021-11-22 16:22

from django.db import migrations
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20211121_1907'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': (django.db.models.expressions.Func(django.db.models.expressions.F('username'), function='Lower'),)},
        ),
    ]
