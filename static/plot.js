var ost = 0;
var nord = 0;
var sor = 0;
var vest = 0;
var xstart;
var xslutt;
var ystart;
var yslutt;
var zoomet;
var xcoords;
var ycoords;
var zcoords;
var myplot = document.getElementById('myDiv')
var id
var nozoom = 0;
var nozoom1 = 0;
var zoom = 0;
var xhover;
var yhover;
var s = 0
var liste;
function Contour(rutenr) {
    
 
    
    id=rutenr
    document.getElementById("3d").disabled = false;
    document.getElementById("contour").disabled = true;

    liste=["178","165","164","179"]
    

    //Definerer variablene som skal sendes til serveren
    var vars = "id=" + liste
    var request = new XMLHttpRequest();
    //Sender POST/GET request til serveren
    request.onreadystatechange = function () {
        if (request.readyState == 4) {
            res = request.response;

            plot(res)
        }
    }
    request.open('POST', 'http://127.0.0.1:5000/firstzoom');
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.send(vars);



}
//Denne functionen må omskrives når den er nødvendig
/*function tilbake_til_contour() {
    document.getElementById("contour-knapp").disabled = true;
    document.getElementById("3d-knapp").disabled = false;
    var vars = "xcoord=" + xstart + "&xcoord1=" + xslutt + "&zoom=" + zoomet

    console.log(zoomet);
    console.log(xstart);
    console.log(xslutt);

    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (request.readyState == 4) {

            res = request.response;
            resp = JSON.parse(res);
            if (resp === undefined || resp.length == 0) {
                console.log("")
            }
            else {
                act_on_resp(res, zoomet);
            }
        }
    }
    request.open('POST', 'http://127.0.0.1:5000/firstzoom');
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.send(vars);

}*/


function plot(resp) {

    coords = JSON.parse(resp);
    //Bestemmer hvor start og slutten for både x og y er
    xstart = coords['xstart']
    xslutt = coords['xslutt']
    ystart = coords['ystart']
    yslutt = coords['yslutt']
    
    //Variabelen som holder listene og instillinger for plotet
    var data = [{
        z: coords["z"],
        x: coords["x"],
        y: coords["y"],

        type: 'contour',

        contours: {
            coloring: 'heatmap'
        },
        colorscale: [
            ['0.0', 'rgb(165,0,38)'],
            ['0.111111111111', 'rgb(215,48,39)'],
            ['0.222222222222', 'rgb(244,109,67)'],
            ['0.333333333333', 'rgb(253,174,97)'],
            ['0.444444444444', 'rgb(254,224,144)'],
            ['0.555555555556', 'rgb(224,243,248)'],
            ['0.666666666667', 'rgb(171,217,233)'],
            ['0.777777777778', 'rgb(116,173,209)'],
            ['0.888888888889', 'rgb(69,117,180)'],
            ['1.0', 'rgb(49,54,149)']
        ],
        
        line: {
            smoothing: 0.85
        },
        coonectgaps: true,

        autocontour: false,


    }];
    var layout = {
        autosize: true,
        showlegend: false,
        title: 'Basic Contour Plot',
        width: 800,
        height: 800
    }



    //Lager plotet
    Plotly.newPlot('myDiv', data, layout, { scrollZoom: true });
    //reseter plotet til start zoom visst du dobbel klikker
    myDiv.on('plotly_doubleclick', function () {
            console.log(zoom)
            plotreset();
        
    });
    //Henter informasjon om hvor musen ligger på kartet, brukt til å zoome rundt musen
    myDiv.on('plotly_hover', function (data) {
        var infotext = data.points.map(function (d) {

            xhover = d.x
            yhover = d.y

        });
    })
    //onscroll så zoomer du
    myDiv.on('plotly_relayout',
        function () {
            plotzoom();
        });
    myDiv.on('plotly_click',
        function () {
            if (zoom == 0) {
                
            }
            else {
                setTimeout(function () {
                    plotzoomut();
                }, 300);
                
            }
        });

}


function d3get() {

    document.getElementById("3d").disabled = true;
    document.getElementById("contour").disabled = false;

    var vars = "zoom=" + zoom + "&nord=" + nord + "&sor=" + sor + "&vest=" + vest + "&ost=" + ost + "&id=" + liste + "&xstart=" + xstart + "&xslutt=" + xslutt + "&ystart=" + ystart + "&yslutt=" + yslutt

    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (request.readyState == 4) {
            res = request.response;
            console.log(res);
            plot3d(res);


        }
    }
    request.open('POST', 'http://127.0.0.1:5000/zoom');
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.send(vars);

}

function plot3d(res) {
    var coords = []
    coords = JSON.parse(res);
    var test=[];
    for (i = 0; coords['z'].length > i; i++) {
        for (s = 0; coords['z'][i].length > s; s++) {
            if (coords['z'][i][s] == null) {
            }
            else {
                coords['z'][i][s] = -Math.abs(coords['z'][i][s])
            }
        }
    }



        console.log(test)
        console.log(coords['z'][7][2])
    var data = [{
        x: coords["x"],
        y: coords["y"],
            z: coords["z"],
        type: 'surface',
        contours: {
            z: {
                show: true,
                usecolormap: true,
                highlightcolor: "#42f462",
                project: { z: true }
            }
        }
        }];
    var layout = {
        title: 'Mt Bruno Elevation',
        scene: { camera: { eye: { x: 1.87, y: 0.88, z: -0.64 } } },
        autosize: false,
        width: 800,
        height: 800,
        margin: {
            l: 65,
            r: 50,
            b: 65,
            t: 90,
        }
    };
        Plotly.newPlot('myDiv', data, layout);
   
}

function plotreset() {
    nozoom = 1;
    nozoom1=1
    if (zoom == 0) {

    }
    else {

        zoom = 0

        var vars = "&id=" + liste
        var request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (request.readyState == 4) {

                res = request.response;
                resp = JSON.parse(res);
                if (resp === undefined || resp.length == 0) {
                    console.log("")
                }
                else {
                    plot(res);
                }
            }
        }
        request.open('POST', 'http://127.0.0.1:5000/firstzoom');
        request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        request.send(vars);
    }
}
function plotzoom() {
    if (nozoom == 0) {
        if (zoom == 0) {
            lvl = xslutt - xstart+5
        }
        xzoom = xslutt- xhover
        console.log(lvl)
        yzoom = ystart - yhover

        console.log(xstart)
        console.log(yslutt)
        console.log(xhover)
        console.log(yhover)
        ost = xzoom / 8
        vest = lvl/8 - xzoom / 8
        nord = yzoom / 8
        sor = lvl/8 - yzoom / 8
        console.log(nord)
        console.log(sor)
        console.log(ost)
        console.log(vest)




        zoom += 10

        var vars = "zoom=" + zoom + "&nord=" + nord + "&sor=" + sor + "&vest=" + vest + "&ost=" + ost + "&id=" + liste + "&xstart=" + xstart + "&xslutt=" + xslutt + "&ystart=" + ystart + "&yslutt=" + yslutt
        var request = new XMLHttpRequest();
        request.onreadystatechange = function () {
            if (request.readyState == 4) {

                res = request.response;
                resp = JSON.parse(res);
                if (resp === undefined || resp.length == 0) {
                    console.log("")
                }
                else {
                    plot(res, zoomet);
                }
            }
        }
        request.open('POST', 'http://127.0.0.1:5000/zoom');
        request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        request.send(vars);
        nozoom1 = 0;
    }
    else {
        nozoom = 0;
    }
}
function plotzoomut() {
    if (nozoom1 == 0) {

        lvl = xslutt - xstart
        xzoom = xslutt - xhover
        console.log(lvl)
        yzoom = ystart - yhover

        console.log(xstart)
        console.log(yslutt)
        console.log(xhover)
        console.log(yhover)

        zoom -= 10
        if (zoom == 0) {

            var vars =  "&id=" + liste
            var request = new XMLHttpRequest();
            request.onreadystatechange = function () {
                if (request.readyState == 4) {

                    res = request.response;
                    resp = JSON.parse(res);
                    if (resp === undefined || resp.length == 0) {
                        console.log("")
                    }
                    else {
                        plot(res);
                    }
                }
            }
            request.open('POST', 'http://127.0.0.1:5000/firstzoom');
            request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            request.send(vars);
        }
        else {
            ost = -xzoom / 8
            vest = -lvl / 8 + xzoom / 8
            nord =-yzoom / 8
            sor = -lvl / 8 + yzoom / 8
            var vars = "zoom=" + zoom + "&nord=" + nord + "&sor=" + sor + "&vest=" + vest + "&ost=" + ost + "&id=" + liste + "&xstart=" + xstart + "&xslutt=" + xslutt + "&ystart=" + ystart + "&yslutt=" + yslutt
            var request = new XMLHttpRequest();
            request.onreadystatechange = function () {
                if (request.readyState == 4) {

                    res = request.response;
                    resp = JSON.parse(res);
                    if (resp === undefined || resp.length == 0) {
                        console.log("")
                    }
                    else {
                        plot(res);
                    }
                }
            }
            request.open('POST', 'http://127.0.0.1:5000/zoom');
            request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            request.send(vars);
        }
        console.log(nord)
        console.log(sor)
        console.log(ost)
        console.log(vest)




        


    }
    else {
        nozoom1 = 0;
    }
}
