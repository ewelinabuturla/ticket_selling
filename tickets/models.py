from datetime import datetime, timezone
from decimal import Decimal

from django.utils.text import slugify
from django.db import models

class TicketType(models.Model):
    ticket_type = models.CharField('Type', max_length=50, blank=False)
    amount = models.IntegerField('Amount', blank=False)
    price = models.DecimalField('Price', max_digits=6, decimal_places=2, default=Decimal(0.0), blank=False)

    def __str__(self):
        return f'{self.ticket_type} - {self.amount} - {self.price}'

    def available_tickets(self):
        return self.amount

class Event(models.Model):
    name = models.CharField('Name', max_length=70, blank=False)
    description = models.CharField('Description', max_length=255, blank=True)
    time = models.DateTimeField('Time', blank=False)

    def __str__(self):
        return f'{self.name} - {self.time}'

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=False)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.event} - {self.ticket_type}'

class TicketPurchase(models.Model):
    date = models.DateTimeField('Date', auto_now_add=True)
    quantity = models.IntegerField(default=0, blank=False)
    ticket = models.IntegerField() # ticket pk would be handled in frontend
    email = models.EmailField('Email', default='', unique=True)
    status = models.CharField(default='pending', max_length=15)
    total_price = models.DecimalField('Price', max_digits=6, decimal_places=2, default=Decimal(0.0), blank=True)

    def __str__(self):
        return f'{self.email} - {self.ticket}'

    def paid(self):
        return 'paid' in self.status

    @property
    def is_expired(self):
        seconds_to_expire = 900
        if (datetime.now(timezone.utc) - self.date).seconds > seconds_to_expire:
            return True
        else:
            return False
