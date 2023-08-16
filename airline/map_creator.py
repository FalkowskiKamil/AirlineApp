import folium
from folium.vector_layers import PolyLine
import geopy.distance

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
