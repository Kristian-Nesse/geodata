from KonverterGeo import konvertereFraUTM
import folium
import json
import os
import pandas as pd
import utm
import base64
from folium import IFrame,LatLngPopup,FeatureGroup,LayerControl
from folium.plugins import HeatMap,MiniMap,Terminator
from folium.plugins import MousePosition,MeasureControl,Search,Fullscreen
from folium.raster_layers import VideoOverlay

#Til i morgen: Sjå meir på Iframe og dei greine der





def graderView(ur,width,height):
    with open(ur, 'r') as f:
        html = f.read()
    iframe = IFrame(html=html,width=width,height=height)
    popup = folium.Popup(iframe,max_width=width)
    return popup




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




def Info_pop(width,height):
    
    
    Info1 = 'Eit eller anna'                             
    Info2 = 'Eit eller anna'                           
    Info3 = 'Eit eller anna'
    Info4 = 'Eit eller anna'     
    Info5 = 'Eit eller anna'       
    Info6 = 'Eit eller anna'       
    Info7 = 'Eit eller anna'       
    
    left_col_colour = "#2A799C"
    right_col_colour = "#C5DCE7"
    
    html = """<!DOCTYPE html>
<html>

<head>
<h4 style="margin-bottom:0"; width="300px">{}</h4>""".format(Info3) + """

</head>
    <table style="height: 126px; width: 300px;">
<tbody>
<tr>
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Info</span></td>
<td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(Info1) + """
</tr>
<tr>
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Info</span></td>
<td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(Info2) + """
</tr>
<tr>
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Info</span></td>
<td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(Info4) + """
</tr>
<tr>
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Info</span></td>
<td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(Info5) + """
</tr>
<tr>
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Info</span></td>
<td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(Info6) + """
</tr>
<tr>
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Info</span></td>
<td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(Info7) + """
</tr>
</tbody>
</table>
</html>
""" 
    
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

folium.plugins.Fullscreen().add_to(m)
#folium.plugins.Terminator().add_to(m)


feature_group = FeatureGroup(name='Vis ikoner')


minimap = folium.plugins.MiniMap()
m.add_child(minimap)



#folium.LatLngPopup().add_to(m)

# Global tooltip
tooltip = 'Klikk for mer info'

logoIcon = folium.features.CustomIcon('viking.jpg', icon_size=(50, 50))


API_KEY_Sondre='AIzaSyAJ841P4vs4-tZiTV9lKIOPYQnagD3LXXs'

folium.Marker([58.925263, 5.668249],popup=graderView('plottttt.html',400,500),tooltip=tooltip).add_to(feature_group)

url='http://hafrsfjord.org/velkommen-til-funn-hafrsfjord/'


folium.Marker([58.924263, 5.638249],
              popup=Pop_Nettside(url,400,400),
              tooltip=tooltip,
              icon=folium.Icon(icon='cloud')).add_to(feature_group)

folium.Marker([58.928263, 5.618249],
              popup=Info_pop(200,200),
              tooltip=tooltip,
              icon=folium.Icon(color='purple')).add_to(feature_group),
folium.Marker([58.927263, 5.648249],
              popup=graderView('earth.html',700,700),
              tooltip=tooltip,
              icon=folium.Icon(color='green', icon='leaf')).add_to(feature_group),
folium.Marker([58.909999907690874,5.627614114359846],
              popup=popupen,
              tooltip=tooltip,
              icon=logoIcon).add_to(feature_group),
folium.Marker([58.9278263, 5.657249],
              popup=folium.Popup(max_width=450).add_child(folium.Vega(json.load(open('vis.json')), width=450, height=250)),
              icon=folium.Icon(color='orange', icon='leaf')).add_to(feature_group)


#Lager video overlay





#Lager heatmap (egentlig ikkje nødvendig å ha med)
J=konvertereFraUTM('16.asc')[1]
folium.plugins.HeatMap(J,'test',max_zoom=22).add_to(m)




folium.plugins.MousePosition().add_to(m)
folium.plugins.MeasureControl().add_to(m)

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
folium.GeoJson('myfile.json').add_to(feature_group)

<<<<<<< HEAD
=======
J=konvertereFraUTM('txtfiler/16.asc')[1]

print(J)

folium.plugins.HeatMap(J,'test',max_zoom=22).add_to(m)

folium.plugins.MousePosition().add_to(m)
folium.plugins.MeasureControl().add_to(m)
>>>>>>> Server-setup



# Geojson overlay
#folium.GeoJson('hafs.json', name='Harfsfjord').add_to(m)




#Lager kart

folium.raster_layers.VideoOverlay(video_url='https://www.youtube.com/watch?v=L3UjvRvGD54',
                                  bounds=[[58.92910634656433,5.690574645996093],[58.94451828576638,5.741729736328124]],
                                  opacity=0.65,
                                  autoplay=True,
                                  loop=False,
                                  overlay=False
                                  ).add_to(m)


feature_group.add_to(m)
LayerControl().add_to(m)


m.save('kart2.html')


