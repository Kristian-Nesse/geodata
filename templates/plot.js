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

var zoom = 0;
var xhover;
var yhover;
var s = 0
function Contour(id1) {

    id = id1


    //Denne funksjonen kjører når siden blir lastet eller når du zoomer ut

    //Definerer variablene som skal sendes til serveren
    var vars = "id=" + id
    var request = new XMLHttpRequest();

    request.onreadystatechange = function () {
        if (request.readyState == 4) {
            res = request.response;

            act_on_resp(res, id)
        }
    }
    request.open('POST', 'http://127.0.0.1:5000/firstzoom');
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.send(vars);



}
function tilbake_til_contour() {
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

}


function act_on_resp(resp, id) {

    coords = JSON.parse(resp);
    xstart = coords['xstart']
    xslutt = coords['xslutt']
    ystart = coords['ystart']
    yslutt = coords['yslutt']


    var data = [{
        z: coords["z"],
        x: coords["x"],
        y: coords["y"],

        type: 'contour',
        reversescale: true,
        contours: {
            coloring: 'heatmap'
        },
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




    Plotly.newPlot('myDiv', data, layout, { scrollZoom: true });
    myDiv.on('plotly_doubleclick', function () {
        ost = 0
        vest = 0
        sor = 0
        nord = 0
    });

    myDiv.on('plotly_hover', function (data) {
        var infotext = data.points.map(function (d) {

            xhover = d.x
            yhover = d.y

        });
    })
    myDiv.on('plotly_relayout',
        function (eventdata) {

            test(id);





        });

}


function plot3d() {

    document.getElementById("3d-knapp").disabled = true;

    var vars = "zoom=" + zoom + "&nord=" + nord + "&sor=" + sor + "&vest=" + vest + "&ost=" + ost + "&id=" + id

    var request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (request.readyState == 4) {
            res = request.response;
            console.log(res);
            plot(res);


        }
    }
    request.open('POST', 'http://127.0.0.1:5000/treD');
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.send(vars);

}

function plot(res) {
    var coords = []
    coords = JSON.parse(res);

    Plotly.d3.csv('https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv', function (err, rows) {
        function unpack(rows, key) {
            return rows.map(function (row) { return row[key]; });
        }

        /*var z_data = []
        var data = []
        var z=0
        for (i = 0; i < coords['x'].length; i++) {
            data[z] = coords['z'][i]
            z++
            if (i %Math.floor(Math.sqrt(coords['z'].length)) == 0) {
                if (i > 2) {
                    z_data.push(data);
                    data = []
                    z = 0
                }
            }
            console.log(coords['z'].length)
        }
        console.log(z_data)
        */
        console.log(coords)
        console.log(coords.length)
        var data = [{
            z: coords,
            type: 'surface',
            reversescale: true
        }];

        var layout = {
            title: 'Kart over Hafsfjorden mellom ' + xstart + " og " + xslutt,
            autosize: false,
            width: 1000,
            height: 600,
            margin: {
                l: 65,
                r: 50,
                b: 65,
                t: 90,
            }
        };
        Plotly.newPlot('myDiv', data, layout);
    });
}

function test() {

    xzoom = xslutt - xhover
    yzoom = yslutt - yhover
    ost = ost + xzoom / 8
    vest = vest + 25 - xzoom / 8
    nord = nord + yzoom / 8
    sor = sor + 25 - yzoom / 8
    console.log(nord)
    console.log(sor)
    console.log(ost)
    console.log(vest)




    zoom += 10

    var vars = "zoom=" + zoom + "&nord=" + nord + "&sor=" + sor + "&vest=" + vest + "&ost=" + ost + "&id=" + id
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
    request.open('POST', 'http://127.0.0.1:5000/test2');
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.send(vars);
}