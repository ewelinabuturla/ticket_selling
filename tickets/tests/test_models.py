from django.test import TestCase
from ..models import (
    TicketType,
    Event,
    Ticket,
    TicketPurchase
)


class TicketsTest(TestCase):
    """
    Test module for models
    """
    def setUp(self):
        self.ticket_type_1 = TicketType.objects.create(
            id=1,
            ticket_type='VIP ticket',
            amount=100,
            price=150
        )
        self.ticket_type_2 = TicketType.objects.create(
            id=2,
            ticket_type='Regular ticket',
            amount=80,
            price=100
        )
        self.ticket_type_3 = TicketType.objects.create(
            id=3,
            ticket_type='Normal ticket',
            amount=50,
            price=30
        )
        self.event_1 = Event.objects.create(
            id=1,
            name='Piano concert',
            description='Live piano music',
            time='2019-08-09T19:06:19Z'
        )
        self.event_2 = Event.objects.create(
            id=2,
            name='Hip-hop music',
            description='Hip-hop show!',
            time='2019-08-19T19:06:19Z'
        )
        self.ticket_1 = Ticket.objects.create(
            id=1,
            event=self.event_1,
            ticket_type=self.ticket_type_1
        )
        self.ticket_2 = Ticket.objects.create(
            id=2,
            event=self.event_2,
            ticket_type=self.ticket_type_2
        )
        self.ticket_3 = Ticket.objects.create(
            id=3,
            event=self.event_2,
            ticket_type=self.ticket_type_3
        )
        self.purchase_ticket_1 = TicketPurchase.objects.create(
            id=1,
            date='2019-08-13T19:06:19Z',
            quantity=10,
            ticket=1,
            email='some-email@email.com',
            total_price=1500
        )
        self.purchase_tickt_2 = TicketPurchase.objects.create(
            id=2,
            date='2019-08-13T19:06:19Z',
            quantity=1,
            ticket=2,
            email='another-emil@email.com',
            total_price=200
        )

    def test_ticket_type_amount(self):
        ticket_1 = TicketType.objects.get(pk=1)
        ticket_2 = TicketType.objects.get(pk=2)
        self.assertEqual(
            ticket_1.amount, 100)
        self.assertEqual(
            ticket_2.amount, 80)

    def test_event_name(self):
        event_1 = Event.objects.get(pk=1)
        event_2 = Event.objects.get(pk=2)
        self.assertEqual(
            event_1.name, 'Piano concert')
        self.assertEqual(
            event_2.name, 'Hip-hop music')

    def test_ticket_event(self):
        ticket_1 = Ticket.objects.get(pk=1)
        ticket_2 = Ticket.objects.get(pk=2)
        self.assertEqual(
            ticket_1.event, self.event_1)
        self.assertEqual(
            ticket_2.event, self.event_2)

    def test_purchase_ticket_quantity(self):
        ticket_1 = TicketPurchase.objects.get(pk=1)
        ticket_2 = TicketPurchase.objects.get(pk=2)
        self.assertEqual(
            ticket_1.quantity, 10)
        self.assertEqual(
            ticket_2.quantity, 1)
