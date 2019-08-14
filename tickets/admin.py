from django.contrib import admin

from .models import Ticket, Event, TicketType, TicketPurchase

# Register your models here.
admin.site.register(Ticket)
admin.site.register(Event)
admin.site.register(TicketType)
admin.site.register(TicketPurchase)
