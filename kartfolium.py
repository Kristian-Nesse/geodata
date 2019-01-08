from KonverterGeo import konvertereFraUTM
import folium
import json
import os
import pandas as pd
import utm
import base64
from folium import IFrame
from folium.plugins import HeatMap
from folium.plugins import MousePosition,MeasureControl,Search


#Til i morgen: Sjå meir på Iframe og dei greine der



def Pop_Nettside(url,width,height):
    html = """ 
            <!doctype html>
        <html>
        <iframe id="myIFrame" width="{}" height="{}" src={}""".format(width,height,url) + """ frameborder="0"></iframe>
        <script type="text/javascript">
        var resizeIFrame = function(event) {
            var loc = document.location;
            if (event.origin != loc.protocol + '//' + loc.host) return;

            var myIFrame = document.getElementById('myIFrame');
            if (myIFrame) {
                myIFrame.style.height = event.data.h + "px";
                myIFrame.style.width  = event.data.w + "px";
            }
        };
        if (window.addEventListener) {
            window.addEventListener("message", resizeIFrame, false);
        } else if (window.attachEvent) {
            window.attachEvent("onmessage", resizeIFrame);
        }
        </script>
        </html>"""

    iframe = IFrame(html=html,width=width,height=height)
    popup = folium.Popup(iframe,max_width=width)
    return popup





def Pop_JPEG(bildenavn):
    encoded = base64.b64encode(open('plotbilde.jpg', 'rb').read()).decode()

    html = '<img src="data:image/jpeg;base64,{}">'.format
    iframe = IFrame(html(encoded), width=632+20, height=420+20)
    popupen = folium.Popup(iframe, max_width=2650)
    return popupen


popupen=Pop_JPEG('plotbilde.jpg')


# Create map object
m = folium.Map(location=[58.923263, 5.648249], zoom_start=12)

# Global tooltip
tooltip = 'Klikk for mer info'

logoIcon = folium.features.CustomIcon('viking.jpg', icon_size=(50, 50))


folium.Marker([58.925263, 5.668249],'<strong>Location one</strong>',tooltip).add_to(m)

url='http://hafrsfjord.org/velkommen-til-funn-hafrsfjord/'

folium.Marker([58.924263, 5.638249],
              popup=Pop_Nettside(url,400,400),
              tooltip=tooltip,
              icon=folium.Icon(icon='cloud')).add_to(m)

folium.Marker([58.928263, 5.618249],
              popup='<strong>Location Three</strong>',
              tooltip=tooltip,
              icon=folium.Icon(color='purple')).add_to(m),
folium.Marker([58.927263, 5.648249],
              popup='<strong>Location Four</strong>',
              tooltip=tooltip,
              icon=folium.Icon(color='green', icon='leaf')).add_to(m),
folium.Marker([58.909999907690874,5.627614114359846],
              popup=popupen,
              tooltip=tooltip,
              icon=logoIcon).add_to(m),
folium.Marker([58.9278263, 5.657249],
              popup=folium.Popup(max_width=450).add_child(folium.Vega(json.load(open('vis.json')), width=450, height=250)),
              icon=folium.Icon(color='orange', icon='leaf')).add_to(m)


# Circle marker
#folium.CircleMarker(
    #location=[58.92263, 5.658249],
   # radius=50,
   # popup='My Birthplace',
  #  color='#428bca',
 #   fill=True,
 #   fill_color='#428bca'
#).add_to(m)

#m.choropleth(geo_data='firkant.json',line_color=None)

#folium.GeoJson('firkant.json', name='Harfsfjord').add_to(m)
folium.GeoJson('myfile.json', name='haloen').add_to(m)

J=konvertereFraUTM('16.asc')[1]

print(J)

folium.plugins.HeatMap(J,'test',max_zoom=22).add_to(m)

folium.plugins.MousePosition().add_to(m)
folium.plugins.MeasureControl().add_to(m)



# Geojson overlay
#folium.GeoJson('hafs.json', name='Harfsfjord').add_to(m)


#Lager kart
m.save('kart2.html')


