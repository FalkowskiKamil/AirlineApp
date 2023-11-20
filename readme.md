# AirlinesApp

AirlinesApp is a Django-based application that allows users to import real data about airports and create fake connections (flights) between them. The app provides features such as displaying airports on a map, creating routes between airports, and allowing users to sign up for flights.


## Overview
[You can have an overview of the functionality of the app on this site](http://airline.falkowskikamil.site/)


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
![Screenshot 2023-08-29 at 15-40-14 Airline](https://github.com/FalkowskiKamil/AirlineApp_django/assets/116383333/4b24a7d4-ab3a-4987-83be-615cd5d3bff1)
![Screenshot 2023-08-29 at 15-40-42 Airline](https://github.com/FalkowskiKamil/AirlineApp_django/assets/116383333/481fb262-9665-4825-9603-0063ed6b0ff2)
![Screenshot 2023-08-29 at 15-37-03 Airline](https://github.com/FalkowskiKamil/AirlineApp_django/assets/116383333/83c4b93c-dfe9-4965-b94d-8c2e4d918bd2)
![Screenshot 2023-08-29 at 15-41-55 Flight Number 51](https://github.com/FalkowskiKamil/AirlineApp_django/assets/116383333/e48b06eb-c099-4335-8086-905ac89b3e4a)
![Screenshot 2023-08-29 at 15-41-44 Route number 47](https://github.com/FalkowskiKamil/AirlineApp_django/assets/116383333/658fc5b0-a8b7-4035-978b-ed4a15964833)
![Screenshot 2023-08-29 at 15-41-21 Ifrane Airport](https://github.com/FalkowskiKamil/AirlineApp_django/assets/116383333/d80f3b1e-2e23-4c5b-8bd9-015fc522ec4b)
![Screenshot 2023-08-29 at 15-41-09 Passager 123 123](https://github.com/FalkowskiKamil/AirlineApp_django/assets/116383333/8eb352c1-d459-4e1c-a16b-b2b2e19b6393)
![Screenshot 2023-08-29 at 15-41-02 Airline](https://github.com/FalkowskiKamil/AirlineApp_django/assets/116383333/930a0d6a-1b19-4d20-980d-90b1a284729c)


## Technologies Used

- Django
- Bootstrap
- Folium
- Faker
- Selenium
- Pytest
- SQLite
- MongoDB
- Docker
- Kubernetes
- Logger

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

## Contribution

Contributions to AirlinesApp are welcome! If you have any ideas or improvements, feel free to submit a pull request.
