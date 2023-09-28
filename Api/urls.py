from . import views
from django.urls import path

urlpatterns = [
    path('api/ticket/create', views.addTicketApi, name='apicreateticket'),
    path('api/ticket/all', views.allTicketsAPi, name='apigetalltickets'),
    path('api/event/create', views.addEvent, name='apicreateevent'),
    path('api/event/all', views.allEventsAPi, name='apigetallevents'),
    path('api/category/create', views.addCategory, name='apicreatecategory'),
    ]
    
