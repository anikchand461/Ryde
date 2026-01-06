# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import VehicleForm

@login_required
def add_vehicle(request):
    if request.user.user_type != 'owner':
        messages.error(request, "Only vehicle owners can add vehicles.")
        return redirect('home')

    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user
            vehicle.save()
            messages.success(request, f"{vehicle.name} ({vehicle.vehicle_number}) added successfully!")
            return redirect('home')
    else:
        form = VehicleForm()

    return render(request, 'core/add_vehicle.html', {'form': form})
