# services/forms.py
from django import forms
from .models import RepairShop, TowingProvider
from core.models import Location, VEHICLE_TYPE_CHOICES, CAR_ISSUES, BIKE_ISSUES, OTHER_VEHICLE_ISSUES

class RepairShopForm(forms.ModelForm):
    vehicle_types = forms.MultipleChoiceField(choices=VEHICLE_TYPE_CHOICES, widget=forms.CheckboxSelectMultiple)
    car_issues = forms.MultipleChoiceField(choices=CAR_ISSUES, widget=forms.CheckboxSelectMultiple, required=False)
    bike_issues = forms.MultipleChoiceField(choices=BIKE_ISSUES, widget=forms.CheckboxSelectMultiple, required=False)
    other_issues = forms.MultipleChoiceField(choices=OTHER_VEHICLE_ISSUES, widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = RepairShop
        fields = ['vehicle_types', 'car_issues', 'bike_issues', 'other_issues', 'timings', 'amenities']

    # Location will be handled separately or via API


class TowingProviderForm(forms.ModelForm):
    vehicle_types = forms.MultipleChoiceField(choices=VEHICLE_TYPE_CHOICES, widget=forms.CheckboxSelectMultiple)
    
    class Meta:
        model = TowingProvider
        fields = ['vehicle_types', 'towing_types', 'response_time', 'timings', 'amenities']