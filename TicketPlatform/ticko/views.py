from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import EventForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserCreationForm()

    # Always return this at the end for both GET and invalid POST
    return render(request, 'ticko/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'ticko/login.html')


@login_required
def dashboard_view(request):
    return render(request, 'ticko/dashboard.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

@login_required
def event_list_view(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'ticko/event_list.html', {'events': events})

@login_required
def event_detail_view(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'ticko/event_detail.html', {'event': event})

@login_required
def create_event_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'ticko/create_event.html', {'form': form})
@login_required
def book_ticket_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Prevent overbooking
    if event.available_seats <= 0:
        messages.error(request, "Sorry, no seats are available for this event.")
        return redirect('event_detail', event_id=event.id)

    # Check if user already booked
    existing_ticket = Ticket.objects.filter(user=request.user, event=event).first()
    if existing_ticket:
        messages.info(request, "You already booked a ticket for this event.")
        return redirect('event_detail', event_id=event.id)

    # Create ticket
    Ticket.objects.create(user=request.user, event=event, status='reserved')

    # Reduce available seats
    event.available_seats -= 1
    event.save()

    messages.success(request, "Ticket successfully reserved!")
    return redirect('my_tickets')

@login_required
def my_tickets_view(request):
    tickets = Ticket.objects.filter(user=request.user).select_related('event')
    return render(request, 'ticko/my_tickets.html', {'tickets': tickets})

def home_view(request):
    return render(request, 'ticko/home.html')
