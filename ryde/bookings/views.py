# bookings/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.views.generic import ListView, DetailView

from .models import Booking
from .forms import BookingCreateForm
from core.models import Location
from services.models import RepairShop, TowingProvider

@login_required
def create_booking_step1(request):
    """Step 1: Choose service type and issue"""
    if request.user.user_type != 'owner':
        messages.error(request, "Only vehicle owners can create bookings.")
        return redirect('home')

    vehicles = request.user.vehicles.all()
    if not vehicles:
        messages.warning(request, "Please add a vehicle first.")
        return redirect('home')  # Later: add vehicle page

    if request.method == 'POST':
        form = BookingCreateForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.owner = request.user
            booking.save()
            return redirect('create_booking_step2', booking.id)
    else:
        form = BookingCreateForm()
        form.fields['vehicle'].queryset = vehicles

    return render(request, 'bookings/create_step1.html', {'form': form})


@login_required
def create_booking_step2(request, booking_id):
    """Step 2: Set current location and show map with providers"""
    booking = get_object_or_404(Booking, id=booking_id, owner=request.user, status='pending')

    providers = []
    if booking.service_type == 'repair':
        providers = RepairShop.objects.filter(vehicle_types__contains=[booking.vehicle.vehicle_type])
    elif booking.service_type == 'towing':
        providers = TowingProvider.objects.filter(vehicle_types__contains=[booking.vehicle.vehicle_type])

    # Filter providers with location
    providers = providers.exclude(location__isnull=True).annotate(
        distance=Distance('location__point', booking.user_location) if booking.user_location else None
    )

    context = {
        'booking': booking,
        'providers': providers,
        'google_maps_api_key': 'YOUR_GOOGLE_MAPS_API_KEY'  # Replace later with settings
    }
    return render(request, 'bookings/create_step2.html', context)


@login_required
def select_provider(request, booking_id, provider_id):
    """Select provider and finalize booking"""
    booking = get_object_or_404(Booking, id=booking_id, owner=request.user, status='pending')

    if booking.service_type == 'repair':
        provider = get_object_or_404(RepairShop, id=provider_id)
        booking.repair_shop = provider
    else:
        provider = get_object_or_404(TowingProvider, id=provider_id)
        booking.towing_provider = provider

    booking.save()
    messages.success(request, f"Booking request sent to {provider}")
    return redirect('booking_detail', booking.id)


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, owner=request.user)
    if booking.can_cancel():
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, "Booking cancelled successfully.")
    else:
        messages.error(request, "Cannot cancel booking after 2 minutes.")
    return redirect('my_bookings')


class MyBookingsView(ListView):
    model = Booking
    template_name = 'bookings/my_bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(owner=self.request.user)


class ProviderBookingsView(ListView):
    model = Booking
    template_name = 'bookings/provider_bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'repair_shop':
            return Booking.objects.filter(repair_shop=user.repairshop_profile)
        elif user.user_type == 'towing':
            return Booking.objects.filter(towing_provider=user.towingprovider_profile)
        return Booking.objects.none()


@login_required
def accept_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, status='pending')
    if booking.provider_user != request.user:
        messages.error(request, "Not authorized.")
        return redirect('provider_bookings')
    
    booking.status = 'accepted'
    booking.accepted_at = timezone.now()
    booking.save()
    messages.success(request, "Booking accepted!")
    return redirect('provider_bookings')