# Generated by Django 2.1 on 2019-08-12 10:25

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0009_auto_20190812_1013'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TicketReservation',
        ),
        migrations.AddField(
            model_name='ticketpurchase',
            name='status',
            field=models.CharField(default='pending', max_length=15),
        ),
        migrations.AddField(
            model_name='ticketpurchase',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), max_digits=6, verbose_name='Price'),
        ),
    ]
