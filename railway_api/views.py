from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.db import transaction
import json
from .models import User, Train, Booking


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        role = data.get('role', 'User')  # Default to 'User'

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        user = User.objects.create(
            username=username,
            password=make_password(password),
            role=role
        )
        return JsonResponse({'message': 'User registered successfully'}, status=201)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            return JsonResponse({
                'message': 'Login successful',
                'access_token': str(access_token)
            }, status=200)

        return JsonResponse({'error': 'Invalid credentials'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
@staff_member_required  # Ensures that only admin users can add trains
def add_train(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        source = data.get('source')
        destination = data.get('destination')
        total_seats = data.get('total_seats')

        if Train.objects.filter(name=name, source=source, destination=destination).exists():
            return JsonResponse({'error': 'Train already exists on this route'}, status=400)

        train = Train.objects.create(
            name=name,
            source=source,
            destination=destination,
            total_seats=total_seats,
            available_seats=total_seats  # Initially, available seats = total seats
        )
        return JsonResponse({'message': 'Train added successfully'}, status=201)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def get_seat_availability(request):
    if request.method == 'GET':
        source = request.GET.get('source')
        destination = request.GET.get('destination')

        if not source or not destination:
            return JsonResponse({'error': 'Source and destination are required'}, status=400)

        trains = Train.objects.filter(source=source, destination=destination)

        if not trains:
            return JsonResponse({'error': 'No trains found on this route'}, status=404)

        train_data = [
            {
                'name': train.name,
                'source': train.source,
                'destination': train.destination,
                'available_seats': train.available_seats
            } for train in trains
        ]
        
        return JsonResponse({'trains': train_data}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def book_seat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        train_id = data.get('train_id')

        try:
            train = Train.objects.get(id=train_id)
        except Train.DoesNotExist:
            return JsonResponse({'error': 'Train not found'}, status=404)

        if train.available_seats <= 0:
            return JsonResponse({'error': 'No available seats on this train'}, status=400)

        with transaction.atomic():  # Ensures that the booking is atomic
            train.available_seats -= 1
            train.save()
            booking = Booking.objects.create(user=request.user, train=train)
        
        return JsonResponse({'message': 'Seat booked successfully', 'booking_id': booking.id}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
def get_booking_details(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
        response_data = {
            "train": booking.train.name,
            "source": booking.train.source,
            "destination": booking.train.destination,
            "seats_booked": booking.seats_booked,
        }
        return JsonResponse(response_data, status=200)
    except Booking.DoesNotExist:
        return JsonResponse({"error": "Booking not found"}, status=404)
