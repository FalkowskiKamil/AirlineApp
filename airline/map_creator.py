import folium
from folium.vector_layers import PolyLine
import geopy.distance
import random

def create_map(airport_start, airport_dest=None):
    if airport_dest:
        # If there's a destination airport, set the center of the map to the midpoint
        center_latitude = (airport_start.latitude + airport_dest.latitude) / 2
        center_longitude = (airport_start.longitude + airport_dest.longitude) / 2

        cord_start = (airport_start.latitude, airport_start.longitude)
        cord_destination = (airport_dest.latitude, airport_dest.longitude)
        distance = geopy.distance.geodesic(cord_start, cord_destination).km
        if distance > 5000:
            zoom_level = 2  
        else:
            zoom_level = 4
    else:
        center_latitude = airport_start.latitude
        center_longitude = airport_start.longitude
        zoom_level = 10

    map = folium.Map(
        location=[center_latitude, center_longitude],
        zoom_start=zoom_level,
        height=250,
    )
    
    folium.Marker(
        location=[airport_start.latitude, airport_start.longitude],
        popup=airport_start.name,
        icon=folium.Icon(color="green"),
    ).add_to(map)

    if airport_dest:
        folium.Marker(
            location=[airport_dest.latitude, airport_dest.longitude],
            popup=f"Destination: {airport_dest.name}",
            icon=folium.Icon(color="red"),
        ).add_to(map)
        line = PolyLine(
            locations=[
                [airport_start.latitude, airport_start.longitude],
                [airport_dest.latitude, airport_dest.longitude],
            ],
            color="blue",
            weight=2,
            opacity=10,
        )
        line.add_to(map)


        distance_text = f"Distance: {distance:.2f} km"

        div_icon = folium.DivIcon(
            html=f'<div style="font-weight: bold; color: red; border: solid 1px;">{distance_text}</div>',
            icon_size=(150, 40)
        )
        # Add the distance DivIcon to the map
        folium.Marker(
            location=[(airport_start.latitude + airport_dest.latitude) / 2,
                      (airport_start.longitude + airport_dest.longitude) / 2],
            icon=div_icon
        ).add_to(map)

    return map

def create_full_map(route_list):
    map = folium.Map(
        location=[0,0],
        zoom_start=2
    )
    for route in route_list:
        folium.Marker(
            location=[route.start.latitude, route.start.longitude],
            popup=f'<a href=/airline/airport/{route.start.airport_id}>Start: {route.start.name}</a>',
            icon=folium.Icon(color="green"),
        ).add_to(map)
        folium.Marker(
            location=[route.destination.latitude+0.01, route.destination.longitude],
            popup=f'<a href=/airline/airport/{route.destination.airport_id}>Destination: {route.destination.name}</a>',
            icon=folium.Icon(color="red"),
        ).add_to(map)
        line = PolyLine(
            locations=[
                [route.start.latitude, route.start.longitude],
                [route.destination.latitude+0.01, route.destination.longitude],
            ],
            color=f'{get_random_color()}',
            weight=2,
            opacity=10,
            popup=f"<a href=/airline/routes/{route.id}>Route '{route.id}' Details</a>",
            tooltip=f"<a href=/airline/routes/{route.id}>Route from: '{route.start.name}', to: '{route.destination.name}'</a>"

        )
        line.add_to(map)
    return map

def get_random_color():
    color = random.randrange(0, 2**24)
    hex_color = hex(color)
    std_color = "#" + hex_color[2:]
    return std_color