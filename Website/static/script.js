/**
 * Js.
 */
// var API_KEY = 'AIzaSyDAPV7m3xJuLkXdEFXP1UAGV2-AcY9QJjU';
var customLabel = {
    restaurant: {
        label: 'R'
    },
    bar: {
        label: 'B'
    }
};

function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
        center: new google.maps.LatLng(-33.863276, 151.207977),
        zoom: 12
    });
    var infoWindow = new google.maps.InfoWindow;

      // Change this depending on the name of your server or XML file
    downloadUrl('https://storage.googleapis.com/mapsdevsite/json/mapmarkers2.xml', function(data) {
        var xml = data.responseXML;
        var markers = xml.documentElement.getElementsByTagName('marker');
        Array.prototype.forEach.call(markers, function(markerElem) {
            var name = markerElem.getAttribute('name');
            var address = markerElem.getAttribute('address');
            var type = markerElem.getAttribute('type');
            var point = new google.maps.LatLng(
              parseFloat(markerElem.getAttribute('lat')),
              parseFloat(markerElem.getAttribute('lng')));

            var infowincontent = document.createElement('div');
            var strong = document.createElement('strong');
            strong.textContent = name;
            infowincontent.appendChild(strong);
            infowincontent.appendChild(document.createElement('br'));

            var text = document.createElement('text');
            text.textContent = address;
            infowincontent.appendChild(text);

            var rating = document.createElement('div');
            rating.setAttribute('class', 'marker-rating');
            for(var i in [1, 2, 3, 4, 5]) {

                if(i < 4) {
                    var star = document.createElement('span');
                    star.setAttribute('class', 'glyphicon glyphicon-star');
                    star.setAttribute('aria-hiden', 'true');
                    rating.appendChild(star)
                } else {
                    var emptyStar = document.createElement('span');
                    emptyStar.setAttribute('class', 'glyphicon glyphicon-star-empty');
                    emptyStar.setAttribute('aria-hiden', 'true');
                    rating.appendChild(emptyStar)
                }

            }

            infowincontent.appendChild(document.createElement('br'));
            infowincontent.appendChild(rating);


            var icon = customLabel[type] || {};
            var marker = new google.maps.Marker({
                map: map,
                position: point,
                label: icon.label
            });
            marker.addListener('click', function() {
                infoWindow.setContent(infowincontent);
                infoWindow.open(map, marker);
            });
        });
    });
}

function downloadUrl(url, callback) {
    var request = window.ActiveXObject ?
        new ActiveXObject('Microsoft.XMLHTTP') :
        new XMLHttpRequest;

    request.onreadystatechange = function() {
        if (request.readyState == 4) {
            request.onreadystatechange = doNothing;
            callback(request, request.status);
        }
    };

    request.open('GET', url, true);
    request.send(null);
}

function doNothing() {}
