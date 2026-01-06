# services/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RepairShopForm, TowingProviderForm
from core.models import Location

@login_required
def setup_profile(request):
    user = request.user
    if user.user_type == 'repair_shop':
        try:
            profile = user.repairshop_profile
        except RepairShop.DoesNotExist:
            profile = None
        form_class = RepairShopForm
    elif user.user_type == 'towing':
        try:
            profile = user.towingprovider_profile
        except TowingProvider.DoesNotExist:
            profile = None
        form_class = TowingProviderForm
    else:
        messages.error(request, 'Only service providers can set up profiles.')
        return redirect('home')

    if request.method == 'POST':
        form = form_class(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            # Handle location (for now, dummy; later auto-detect)
            if not profile.location:
                profile.location = Location.objects.create(name=f"{user}'s Location")
            profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = form_class(instance=profile)

    return render(request, 'services/setup_profile.html', {'form': form, 'user_type': user.user_type})


@login_required
def view_provider_profile(request):
    user = request.user
    if user.user_type == 'repair_shop':
        profile = user.repairshop_profile
    elif user.user_type == 'towing':
        profile = user.towingprovider_profile
    else:
        return redirect('home')

    return render(request, 'services/provider_profile.html', {'profile': profile})