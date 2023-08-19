import folium
from folium.vector_layers import PolyLine
import geopy.distance
import random


def create_map(airport_start, airport_destination=None):
    # Setting basic data
    center_latitude = airport_start.latitude
    center_longitude = airport_start.longitude
    zoom_level = 10

    # Setting for map, when destination
    if airport_destination:
        # Setting coordinations for quickest path
        cord_destination = (
            airport_destination.latitude,
            meridian_calculator(airport_start.longitude, airport_destination.longitude),
        )
        cord_start = (airport_start.latitude, airport_start.longitude)

        center_latitude = (airport_start.latitude + airport_destination.latitude) / 2
        center_longitude = (airport_start.longitude + cord_destination[1]) / 2

        distance = geopy.distance.geodesic(cord_start, cord_destination).km

        zoom_level = 4
        if distance > 5000:
            zoom_level = 2

    map = folium.Map(
        location=[center_latitude, center_longitude],
        zoom_start=zoom_level,
        height=250,
    )

    folium.Marker(
        location=[airport_start.latitude, airport_start.longitude],
        popup=airport_start.name,
        tooltip=airport_start.name,
        icon=folium.Icon(color="green"),
    ).add_to(map)

    if airport_destination:
        folium.Marker(
            location=[cord_destination[0], cord_destination[1]],
            popup=f"Destination: {airport_destination.name}",
            tooltip=f"Destination: {airport_destination.name}",
            icon=folium.Icon(color="red"),
        ).add_to(map)
        line = PolyLine(
            locations=[
                [cord_start[0], cord_start[1]],
                [cord_destination[0], cord_destination[1]],
            ],
            color="blue",
            weight=2,
            tooltip=f"From {airport_start.country} to {airport_destination.country}",
            opacity=10,
        )
        line.add_to(map)

        distance_text = f"Distance: {distance:.2f} km"

        div_icon = folium.DivIcon(
            html=f'<div style="font-weight: bold; color: red; border: solid 1px;">{distance_text}</div>',
            icon_size=(150, 40),
        )
        # Add the distance DivIcon to the map
        folium.Marker(
            location=[
                (cord_start[0] + cord_destination[0]) / 2,
                (cord_start[1] + cord_destination[1]) / 2,
            ],
            icon=div_icon,
        ).add_to(map)

    return map


def create_full_map(route_list):
    map = folium.Map(location=[0, 0], zoom_start=2)
    for route in route_list:
        folium.Marker(
            location=[route.start.latitude, route.start.longitude],
            popup=f"<a href=/airline/airport/{route.start.airport_id}>Start: {route.start.name}</a>",
            icon=folium.Icon(color="green"),
        ).add_to(map)
        destination_longitude = meridian_calculator(
            route.start.longitude, route.destination.longitude
        )
        folium.Marker(
            location=[route.destination.latitude + 0.01, destination_longitude],
            popup=f"<a href=/airline/airport/{route.destination.airport_id}>Destination: {route.destination.name}</a>",
            icon=folium.Icon(color="red"),
        ).add_to(map)
        line = PolyLine(
            locations=[
                [route.start.latitude, route.start.longitude],
                [route.destination.latitude + 0.01, destination_longitude],
            ],
            color=f"{get_random_color()}",
            weight=2,
            opacity=10,
            popup=f"<a href=/airline/routes/{route.id}>Route '{route.id}' Details</a>",
            tooltip=f"<a href=/airline/routes/{route.id}>Route from: '{route.start.name}', to: '{route.destination.name}'</a>",
        )
        line.add_to(map)
    return map


def get_random_color():
    color = random.randrange(0, 2**24)
    hex_color = hex(color)
    std_color = "#" + hex_color[2:]
    return std_color


def meridian_calculator(airport_start, airport_destination):
    if abs(airport_start - airport_destination) > abs(
        airport_start - (airport_destination - 360)
    ):
        return airport_destination - 360
    elif abs(airport_start - airport_destination) > abs(
        airport_start - (airport_destination + 360)
    ):
        return airport_destination + 360
    else:
        return airport_destination
