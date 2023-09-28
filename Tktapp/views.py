from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import *
from . forms import Ticketform, UserAdminCreationForm, EventForm, CategoryInlineFormset, UserAdminChangeForm, TicketInlineFormset, PasswordChangeCustomForm
from .filters import EventFilter
from django.views import generic
from django.contrib import messages
from django.contrib.auth import authenticate, login as lg, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .pdfrender import PdfRender
from django.utils import timezone


ticket_store = {'event': [], 'price': [], 'serial_no': [], 'ticket_type': []}


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

    event = Event.objects.get(uid=pk)
    event_categories = event.categories_set.all()

    context = {
        'formset': TicketInlineFormset(),
        'object': event,
        'categories': event_categories,

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


@login_required(login_url='/login')
def eventCreate(request):
    form_class = EventForm
    template_name = 'eventcreate.html'
    context = {
        'user': request.user,
        'form': form_class
    }
    return render(request, 'eventcreate.html', context)


@login_required(login_url='/login')
def userProfile(request):

    _user = request.user
    event_count = Event.objects.filter(user=_user).count()
    ticket_count = Ticket.objects.filter(User=_user).count()
    checked_out = Ticket.objects.filter(saved=True).count()
    context = {
        'user': request.user,
        'event_count': event_count,
        'ticket_count': ticket_count,
        'checked_out': checked_out,
    }
    return render(request, 'userprofile.html', context)


@login_required
def editProfile(request):

    if request.method == 'POST':
        form = UserAdminChangeForm(request.POST, instance=request.user)
        pass_form = PasswordChangeCustomForm(request.POST)
        if form.is_valid() or pass_form.is_valid():
            pass_form.save()
            form.save()
        else:
            messages.info(request, 'invalid registration details')

    form = UserAdminChangeForm(instance=request.user)
    pass_form = PasswordChangeCustomForm(request.user)
    context = {'form': form, 'pass_form': pass_form}

    return render(request, 'editprofile.html', context)


@login_required
def myTickets(request):

    _user = request.user
    tickets = Ticket.objects.filter(User=_user)
    if request.method == 'POST':
        form = Ticketform(request.POST)
        print(request.POST['username'])

    context = {
        'user': request.user,
        'tickets': tickets,
    }
    return render(request, 'mytickets.html', context)


@login_required
def tickeTotPdf(request, pk):

    _user = request.user
    ticket = Ticket.objects.get(id=pk)

    today = timezone.now()
    params = {
        'today': today,
        'ticket': ticket,
        'request': request,

    }
    return render(request, 'ticket.html', params)
