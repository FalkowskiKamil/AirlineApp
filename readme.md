This is an airline application built with the Django web framework, consisting of multiple views that display information about airports, flights, passengers, and routes. The app uses the folium library to display maps, pandas to process data from a CSV file, and faker to generate fake data.
    
    main(): This displays a list of countries and all existing routes.

    staff(): This displays all the airports, passengers, and flights in the database, ordered by date.

    passager(passager_id): This displays information about a specific passenger based on the provided passager_id.

    flight(fli_id): This displays information about a specific flight based on the provided fli_id and generates a map using folium to display the start and destination airports.

    airport(airport_id): This displays information about a specific airport based on the provided airport_id and generates a map using folium to display the airport location.

    routes(route_id): This displays information about a specific route based on the provided route_id and generates a map using folium to display the start and destination airports.

    flight_record(passager_id, flight_id): This allows passengers to book a specific flight by adding the passager_id to the passengers attribute of the corresponding Flight object.

    upload_airport(): This is a view that allows staff to upload airport information from a CSV file to the database using pandas. The view generates a specified number of airports from the CSV file randomly and adds them to the database.