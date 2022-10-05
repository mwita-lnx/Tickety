from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import *
from . forms import Ticketform, UserAdminCreationForm, EventForm,CategoryInlineFormset,UserAdminChangeForm,TicketInlineFormset,PasswordChangeCustomForm
from .filters import EventFilter
from django.views import generic
from django.contrib import messages
from django.contrib.auth import authenticate, login as lg, logout
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EventSerializer,TicketSerializer
from rest_framework import permissions
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.utils.crypto import get_random_string
from .pdfrender import PdfRender
from django.utils import timezone


ticket_store = {'event':[],'price':[],'serial_no':[],'ticket_type':[]}


def index(request):

    event = Event.objects.all()
    myFilter = EventFilter(request.GET, queryset=event)
    events = myFilter.qs
    context = {'events': events,
               'myFilter': myFilter
               }
    return render(request, 'index.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                lg(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def register(request):
    context = {}
    form = UserAdminCreationForm
    context = {
        'form': form,
        'is_valid': True
    }
    if request.method == 'POST':
        form = UserAdminCreationForm(request.POST)
        if form.is_valid():
            print('good')
            form.save()
        else:
            messages.info(request, 'invalid registration details')
            print('error')
    return render(request, 'register.html', context)



def eventDetail(request, pk):
    
    event  = Event.objects.get(id=pk)
    event_categories = event.categories_set.all()

    context ={
        'formset': TicketInlineFormset(),
        'object':event,
        'categories':event_categories,

    }
    ticket_formset = TicketInlineFormset(request.POST)
    print(request.POST)
    if ticket_formset.is_valid():
        print(request.POST)
        ticket_formset.save()
    
         
    return render(request, "eventdetail.html", context)


def event(request):

    event = Event.objects.all()
    print(request.GET)
    myFilter = EventFilter(request.GET, queryset=event)
    events = myFilter.qs
    context = {'events': events,
               'myFilter': myFilter
               }
    return render(request, 'events.html', context)



@method_decorator(login_required, name='dispatch')
class EventCreateView(generic.CreateView):
    model = Event
    form_class = EventForm
    template_name = 'eventcreate.html'

    def get_context_data(self, **kwargs):
        context = super(EventCreateView, self).get_context_data(**kwargs)
        context['category_formset'] = CategoryInlineFormset()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        category_formset = CategoryInlineFormset(self.request.POST)
        if form.is_valid() and category_formset.is_valid():
            return self.form_valid(form, category_formset)
        else:
            return self.form_invalid(form, category_formset)

    def form_valid(self, form, category_formset):
        self.object = form.save(commit=False)
        self.object.save()
        # saving Productcat Instances
        categorys = category_formset.save(commit=False)
        for cat in categorys:
            cat.event = self.object
            cat.save()
        return redirect('/')

    def form_invalid(self, form, category_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  category_formset=category_formset
                                  )
        )

@login_required(login_url='/login')
def userProfile(request):

    _user =request.user
    event_count = Event.objects.filter(user=_user).count()
    ticket_count = Ticket.objects.filter(User=_user).count()
    checked_out = Ticket.objects.filter(saved=True).count()
    context = {
        'user':request.user,
        'event_count':event_count,
        'ticket_count':ticket_count,
        'checked_out':checked_out,
        }
    return render(request, 'userprofile.html',context)


@login_required
def editProfile(request):
  
    if request.method == 'POST':
        form = UserAdminChangeForm(request.POST,instance=request.user)
        pass_form = PasswordChangeCustomForm(request.POST)
        if form.is_valid() or pass_form.is_valid():
            pass_form.save()
            form.save()
        else:
            messages.info(request, 'invalid registration details')
    
    form = UserAdminChangeForm(instance=request.user)
    pass_form = PasswordChangeCustomForm(request.user)
    context = {'form': form, 'pass_form':pass_form}

    return render(request, 'editprofile.html', context)



@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def addTicketApi(request):
    request.data._mutable = True
    request.data['User'] = request.user.id
    request.data['serial_no'] = get_random_string(10, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    request.data._mutable = False
    # ticket_store['event'].append(request.data['event'])
    # ticket_store['price'].append(request.data['price'])
    # ticket_store['serial_no'].append(request.data['serial_no'])
    # ticket_store['ticket_type'].append(request.data['ticket_type'])
    item = TicketSerializer(data=request.data)
    print(ticket_store)
    if item.is_valid():
        item.save()
        return Response(item.data)
        
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

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
        data = TicketSerializer(items,many=True)
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)



@login_required
def myTickets(request):

    _user =request.user
    tickets = Ticket.objects.filter(User=_user)
    if request.method == 'POST':
        form = Ticketform(request.POST)
        print(request.POST['username'])
        
    context = {
        'user':request.user,
        'tickets':tickets,
        }
    return render(request, 'mytickets.html',context)

@login_required
def tickeTotPdf(request,pk):

    _user =request.user
    ticket = Ticket.objects.get(id=pk)
   

    today = timezone.now()
    params = {
            'today': today,
            'ticket': ticket,
            'request': request,
            
        }
    return  render(request, 'ticket.html',params)
