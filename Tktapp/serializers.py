from rest_framework import serializers
from .models import Event, Ticket,Categories


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["thumbnail", ]

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'