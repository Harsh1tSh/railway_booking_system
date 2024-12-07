from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('admin/add_train/', views.add_train, name='add_train'),  # Admin-only endpoint
    path('seats/', views.get_seat_availability, name='get_seat_availability'),
    path('book/', views.book_seat, name='book_seat'),
    path('api/booking/<int:booking_id>/', views.get_booking_details, name='get_booking_details'),
]