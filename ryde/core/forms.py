# core/forms.py
from django import forms
from .models import Vehicle, VEHICLE_TYPE_CHOICES  # Import the constant directly

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_type', 'name', 'model', 'vehicle_number']
        widgets = {
            'vehicle_type': forms.RadioSelect(choices=VEHICLE_TYPE_CHOICES),  # Use imported constant
            'name': forms.TextInput(attrs={'placeholder': 'e.g., Maruti Swift', 'class': 'form-control'}),
            'model': forms.TextInput(attrs={'placeholder': 'e.g., VXi 2022', 'class': 'form-control'}),
            'vehicle_number': forms.TextInput(attrs={'placeholder': 'e.g., DL10AB1234', 'class': 'form-control'}),
        }
        labels = {
            'vehicle_type': 'Vehicle Type',
            'name': 'Vehicle Name',
            'model': 'Model/Year',
            'vehicle_number': 'License Plate Number',
        }
