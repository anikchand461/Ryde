# bookings/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_booking_step1, name='create_booking_step1'),
    path('create/<int:booking_id>/location/', views.create_booking_step2, name='create_booking_step2'),
    path('select/<int:booking_id>/<int:provider_id>/', views.select_provider, name='select_provider'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('my/', views.MyBookingsView.as_view(), name='my_bookings'),
    path('provider/', views.ProviderBookingsView.as_view(), name='provider_bookings'),
    path('accept/<int:booking_id>/', views.accept_booking, name='accept_booking'),
    path('<int:pk>/', views.DetailView.as_view(model=Booking, template_name='bookings/detail.html'), name='booking_detail'),
]