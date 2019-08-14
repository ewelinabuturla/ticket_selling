from rest_framework import serializers

from tickets.models import Event, Ticket, TicketType, TicketPurchase

# Serializer defines the API representation
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class TicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = '__all__'

class TicketPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketPurchase
        fields = '__all__'

        def create(self, validated_data):
            return TicketPurchase.objects.create(**validated_data)

        def update(self, instance, validated_data):
            instance.quantity = validated_data.get(
                'quantity',
                instance.quantity
            )
            instance.ticket = validated_data.get(
                'ticket',
                instance.ticket
            )
            instance.email = validated_data.get(
                'email',
                instance.email
            )

            instance.save()
            return instance
