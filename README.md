# Railway Management System - IRCTC Clone

This is a Railway Management System API built for the SDE API Round - IRCTC challenge. The API allows users to register, log in, check seat availability, book seats, and manage train data (admin only). The system is designed to handle simultaneous seat booking requests and prevent race conditions during seat booking.

## Table of Contents
- [Project Overview](#project-overview)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Database Connection Issue](#database-connection-issue)
- [Tech Stack](#tech-stack)
- [Assumptions](#assumptions)

## Project Overview
This project aims to simulate a railway management system like IRCTC where users can:
- Check train availability between two stations.
- View the number of available seats on any train.
- Book a seat if the availability is greater than 0.
- Admin users can add new trains to the system and update train details.

## Installation
Clone the repository to your local machine:
Activate the virtual environment
Install dependencies
Run the server


The server will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## API Endpoints
1. **Register User**  
   `POST /api/register/`  
   **Request body:**
   ```json
   {
     "username": "john_doe",
     "password": "password123",
     "role": "User"
   }
   ```

2. **Login User**  
   `POST /api/login/`  
   **Request body:**
   ```json
   {
     "username": "john_doe",
     "password": "password123"
   }
   ```

3. **Add New Train (Admin only)**  
   `POST /api/admin/add_train/`  
   **Request body:**
   ```json
   {
     "name": "Shatabdi Express",
     "source": "New Delhi",
     "destination": "Lucknow",
     "total_seats": 100
   }
   ```
   *(Requires Authorization header with admin token)*

4. **Get Seat Availability**  
   `GET /api/seats/`  
   **Query parameters:**
   ```json
   {
     "source": "New Delhi",
     "destination": "Lucknow"
   }
   ```

5. **Book a Seat**  
   `POST /api/book/`  
   **Request body:**
   ```json
   {
     "train_id": 1
   }
   ```
   *(Requires Authorization header with user token)*

6. **Get Booking Details**  
   `GET /api/booking/<booking_id>/`  
   *(Requires Authorization header with user token)*

## Database Connection Issue
Due to some issues with the database configuration, the connection to the database is not working as expected. As a result, the application may not persist data or allow seat bookings. However, all other functionality, such as registering users, logging in, checking seat availability, and adding trains (admin only), are working as expected.

I am working on fixing the database connection, and I will update the system once it's resolved.

## Tech Stack
- **Backend:** Django 5.1.4
- **Authentication:** JWT Tokens (using rest_framework_simplejwt)
- **Database:** PostgreSQL (currently not connected due to configuration issues)
- **Deployment:** Local development server

## Assumptions
- The database connection issue is temporary, and the rest of the functionality works as expected in this version.
- API requests need to include a valid Authorization token for booking seats and retrieving booking details.

Feel free to test the API and let me know if you encounter any issues. Thank you!
