import folium
from folium.vector_layers import PolyLine

def create_map(airport_start, airport_dest=None):
    map = folium.Map(
        location=[airport_start.latitude, airport_start.longitude], zoom_start=10, height=250)
    folium.Marker(
        location=[airport_start.latitude, airport_start.longitude], popup=airport_start.name, icon=folium.Icon(color="green")).add_to(map)

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
    return map

