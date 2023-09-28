from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EventSerializer, TicketSerializer,CategoriesSerializer
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.utils.crypto import get_random_string
from Tktapp.models import Ticket,Event

# Create your views here.

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def addTicketApi(request):
    request.data._mutable = True
    request.data['User'] = request.user.id
    request.data['serial_no'] = get_random_string(
        10, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    request.data._mutable = False
    # ticket_store['event'].append(request.data['event'])
    # ticket_store['price'].append(request.data['price'])
    # ticket_store['serial_no'].append(request.data['serial_no'])
    # ticket_store['ticket_type'].append(request.data['ticket_type'])
    item = TicketSerializer(data=request.data)
    if item.is_valid():
        item.save()
        return Response(item.data)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def addEvent(request):
    serializer = EventSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def addCategoriesApi(request):
    request.data._mutable = True
    request.data['User'] = request.user.id
    request.data._mutable = False
    item = CategoriesSerializer(data=request.data)
    if item.is_valid():
        item.save()
        return Response(item.data)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def allTicketsAPi(request):

    # checking for the parameters from the URL
    if request.query_params:
        items = Ticket.objects.filter(**request.query_param.dict())
    else:
        items = Ticket.objects.all()

    # if there is something in items else raise error
    if items:
        data = TicketSerializer(items, many=True)
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def allEventsAPi(request):

    # checking for the parameters from the URL
    if request.query_params:
        items = Event.objects.filter(**request.query_param.dict())
    else:
        items = Event.objects.all()

    # if there is something in items else raise error
    if items:
        data = EventSerializer(items, many=True)
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def addCategory(request):
    serializer = CategoriesSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)