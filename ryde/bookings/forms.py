# bookings/forms.py
from django import forms
from .models import Booking

class BookingCreateForm(forms.ModelForm):
    service_type = forms.ChoiceField(
        choices=Booking.SERVICE_TYPE_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:
        model = Booking
        fields = ['service_type', 'vehicle', 'issue', 'description']
        widgets = {
            'vehicle': forms.RadioSelect,
            'issue': forms.Select,
            'description': forms.Textarea(attrs={'rows': 3}),
        }