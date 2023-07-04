# AirlinesApp

AirlinesApp is a Django-based application that allows users to import real data about airports and create fake connections (flights) between them. The app provides features such as displaying airports on a map, creating routes between airports, and allowing users to sign up for flights.


## Overview
![You can have an overview of the functionality of the app on replit](https://replit.com/@KamilFalkowski/AirlineAppdjango)


## Features

- Import real data about airports including country, coordinates, city, and name
- Create fake connections (flights) between airports to generate routes
- Generate fake passengers and connect them to flights
- Display airports and routes on a map using Folium
- Allow users to sign up for flights and view their signed flights
- User authentication: registration, login, and logout
- Logging of user actions including user creation, login, logout, data upload, and flight signing
- Admin-only access to data upload functionality

## Screenshots
![Screenshot 2023-06-13 at 13-24-23 Airline](https://github.com/FalkowskiKamil/AirlineApp_django/assets/116383333/6e19260c-2058-4b20-b795-b39826fe708f)
![Screenshot 2023-06-13 at 13-24-40 Airline](https://github.com/FalkowskiKamil/AirlineApp_django/assets/116383333/91519aeb-ab2b-4723-b49d-82e099941ff9)
![Screenshot 2023-06-13 at 13-25-11 Airline](https://github.com/FalkowskiKamil/AirlineApp_django/assets/116383333/f56d16b7-c035-4539-974e-c356d63bd71c)
![Screenshot 2023-06-13 at 13-25-50 Airline](https://github.com/FalkowskiKamil/AirlineApp_django/assets/116383333/12f0474d-3886-4b43-b452-1ad6179366ed)
![Screenshot 2023-06-13 at 13-26-24 Airline](https://github.com/FalkowskiKamil/AirlineApp_django/assets/116383333/94313bed-8e91-4354-90a0-5c0bdef18e61)

## Technologies Used

- Django
- Folium
- Faker
- Selenium
- Pytest
- MongoDB
- Docker
- Kubernetes

## Installation

Option 1:
   1. Clone the repository.
   2. Install the necessary dependencies using the command 'pip install -r requirements.txt.'
   3. Start the application by running the command 'python manage.py runserver' in the application folder.
   4. Open your browser and go to [http://localhost:8000/](http://localhost:8000/)
   
Option 2:
   1. Clone the Docker image using the command: 'docker pull falkowskikamil/airlinesapp:air' Make sure Docker is installed.
   2. Run container, using host Ports "8000"
   3. Open your browser and go to [http://localhost:8000/](http://localhost:8000/)

## Usage

- To access the full potential of the website, log in using the username "admin" and the password "admin."
- Register a new user: Users can register by providing a unique username, password, first name, and last name.
- Login: Registered users can log in using their username and password.
- Logout: Users can log out of their accounts.
- Data Upload (Admin Only): Admin users can upload data about airports, flights, and passengers using the provided CSV files.
- Main Page: Users can view a list of countries and select a country to see the available routes.
- Country Page: Users can view the routes within a specific country.
- All Page: Users can view all airports and routes.
- Staff Page (Admin Only): Admin users can view all airports, passengers, and flights, and manage the data.
- Passager Page: Users can view details about a specific passenger.
- Flight Page: Users can view details about a specific flight and sign up for it.
- Airport Page: Users can view details about a specific airport and see it on a map.
- Route Page: Users can view details about a specific route and see it on a map.
-  Add Data Page (Admin Only): Admin users can upload data about airports, flights, and passengers.

## Contribution

Contributions to AirlinesApp are welcome! If you have any ideas or improvements, feel free to submit a pull request.
