from rest_framework import serializers
from .models import Event, Ticket


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["thumbnail", ]

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'