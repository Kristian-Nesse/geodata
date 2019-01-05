
import folium
import json
import os

# Create map object
m = folium.Map(location=[58.923263, 5.648249], zoom_start=12)

# Global tooltip
tooltip = 'Click For More Info'

logoIcon = folium.features.CustomIcon('viking.jpg', icon_size=(50, 50))




# Geojson Data



#Setter opp noko markører

folium.Marker([58.925263, 5.668249],'<strong>Location one</strong>',tooltip).add_to(m)

folium.Marker([58.924263, 5.638249],
              popup='<strong>Location Two</strong>',
              tooltip=tooltip,
              icon=folium.Icon(icon='cloud')).add_to(m),

folium.Marker([58.928263, 5.618249],
              popup='<strong>Location Three</strong>',
              tooltip=tooltip,
              icon=folium.Icon(color='purple')).add_to(m),
folium.Marker([58.927263, 5.648249],
              popup='<strong>Location Four</strong>',
              tooltip=tooltip,
              icon=folium.Icon(color='green', icon='leaf')).add_to(m),
folium.Marker([58.922263, 5.658249],
              popup='<strong>Location Five</strong>',
              tooltip=tooltip,
              icon=logoIcon).add_to(m),
folium.Marker([58.912263, 5.658249],
              popup='<strong>Location Five</strong>',
              tooltip=tooltip,
              icon=logoIcon).add_to(m)

# sirkel markør
folium.CircleMarker(
    location=[58.931104,5.638220],
    radius=25,
    popup='Bakholdsangrep',
    color='#428bca',
    fill=True,
    fill_color='#428bca'
).add_to(m)

# Geojson overlay
#folium.GeoJson('hafs.json', name='Harfsfjord').add_to(m)


#Lager kart
m.save('kart2.html')


