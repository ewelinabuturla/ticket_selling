# Generated by Django 2.1 on 2019-08-11 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_auto_20190811_1445'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='tickets_type',
        ),
    ]