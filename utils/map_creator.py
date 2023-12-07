import random
import folium
from airline.models import Airport
from folium.vector_layers import PolyLine
import geopy.distance
from typing import Optional


def create_map(airport_start: Airport, airport_destination: Optional[Airport] = None) -> folium.Map:
    # Setting basic data
    center_latitude: float = airport_start.latitude
    center_longitude: float = airport_start.longitude
    zoom_level: int = 10

    # Setting for map, when destination
    if airport_destination:
        # Setting coordinations for quickest path
        cord_destination: tuple = (
            airport_destination.latitude,
            meridian_calculator(airport_start.longitude, airport_destination.longitude),
        )
        cord_start: tuple = (airport_start.latitude, airport_start.longitude)

        center_latitude: float = (airport_start.latitude + airport_destination.latitude) / 2
        center_longitude: float = (airport_start.longitude + cord_destination[1]) / 2

        distance: float = geopy.distance.geodesic(cord_start, cord_destination).km

        zoom_level: int = 4
        if distance > 5000:
            zoom_level: int = 2

    map: folium.Map = folium.Map(
        location=[center_latitude, center_longitude],
        zoom_start=zoom_level,
        min_zoom=zoom_level,
        height = 250, # type: ignore
    )

    folium.Marker(
        location=[airport_start.latitude, airport_start.longitude],
        popup=airport_start.name,
        tooltip=airport_start.name,
        icon=folium.Icon(color="green"),
    ).add_to(map)

    if airport_destination:
        folium.Marker(
            location=[cord_destination[0], cord_destination[1]],  # type: ignore
            popup=f"Destination: {airport_destination.name}",
            tooltip=f"Destination: {airport_destination.name}",
            icon=folium.Icon(color="red"),
        ).add_to(map)
        line: PolyLine = PolyLine(
            locations=[
                [cord_start[0], cord_start[1]], # type: ignore
                [cord_destination[0], cord_destination[1]], # type: ignore
            ],
            color="blue",
            weight=2,
            tooltip=f"From {airport_start.country} to {airport_destination.country}",
            opacity=10,
        )
        line.add_to(map)

        distance_text: str = f"Distance: {distance:.2f} km" # type: ignore

        div_icon: folium.DivIcon = folium.DivIcon(
            html=f'<div style="font-weight: bold; color: red; border: solid 1px;">{distance_text}</div>',
            icon_size=(150, 40),
        )
        # Add the distance DivIcon to the map
        folium.Marker(
            location=[
                (cord_start[0] + cord_destination[0]) / 2, # type: ignore
                (cord_start[1] + cord_destination[1]) / 2, # type: ignore
            ],
            icon=div_icon,
        ).add_to(map)

    return map


def create_full_map(route_list: list) -> folium.Map:
    map: folium.Map = folium.Map(location=[0, 0], zoom_start=2, min_zoom=2)
    for route in route_list:
        folium.Marker(
            location=[route.start.latitude, route.start.longitude],
            popup=f"<a href=/airline/airport/{route.start.airport_id} target='_blank' rel='noopener noreferrer'>Start: {route.start.name}</a>",
            icon=folium.Icon(color="green"),
        ).add_to(map)
        destination_longitude: float = meridian_calculator(
            route.start.longitude, route.destination.longitude
        )
        folium.Marker(
            location=[route.destination.latitude + 0.01, destination_longitude],
            popup=f"<a href=/airline/airport/{route.destination.airport_id} target='_blank' rel='noopener noreferrer'>Destination: {route.destination.name}</a>",
            icon=folium.Icon(color="red"),
        ).add_to(map)
        line: PolyLine = PolyLine(
            locations=[
                [route.start.latitude, route.start.longitude],
                [route.destination.latitude + 0.01, destination_longitude],
            ],
            color=f"{get_random_color()}",
            weight=2,
            opacity=10,
            popup=f"<a href=/airline/routes/{route.id} target='_blank' rel='noopener noreferrer'>Route '{route.id}' Details</a> ",
            tooltip=f"<a href=/airline/routes/{route.id} target='_blank' rel='noopener noreferrer'>Route from: '{route.start.name}', to: '{route.destination.name}'</a>",
        )
        line.add_to(map)
    return map


def get_random_color() -> str:
    color: float = random.randrange(0, 2**24)
    hex_color: str = format(color, '06x')
    std_color: str= "#" + hex_color
    return std_color



def meridian_calculator(airport_start: float, airport_destination: float) -> float:
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
