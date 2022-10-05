from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='home'),
    path('login&register', views.login, name='login_register'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('user/profile/', views.userProfile, name='userprofile'),\
    path('user/editprofile/', views.editProfile, name='editprofile'),
    path('events/', views.event, name='eventlist'),
    path('events/<pk>/', views.eventDetail, name='eventdeatail'),
    path('events/create', views.EventCreateView.as_view(), name='eventcreate'),
    path('api/ticket/create', views.addTicketApi, name='apicreateticket'),
    path('api/ticket/all', views.allTicketsAPi, name='apigetalltickets'),
    path('mytickets/image/<pk>/', views.tickeTotPdf, name='ticketpdf'),
    path('mytickets/', views.myTickets, name='mytickets'),
    # path('api-auth/', include('rest_framework.urls')),

]
