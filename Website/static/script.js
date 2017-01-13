/**
 * Js.
 */
// var API_KEY = 'AIzaSyDAPV7m3xJuLkXdEFXP1UAGV2-AcY9QJjU';

$(document).ready(function(){
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
            center: new google.maps.LatLng(36.1699, 115.1398),
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

    // function doNothing() {}
    // initMap()

    var loader = $('.loading');

    loader.hide();
    // $('.loading').bind('ajaxStart', function(){
    //     $(this).show();
    // }).bind('ajaxStop', function(){
    //     $(this).hide();
    // });



    $('#search').on('click', function() {

        var query = $("#query").val();

        var request = $.ajax({
          url: "/query",
          method: "POST",
          data: { query : query },
        beforeSend: function(){
            loader.show();
        },
          dataType: "json"
        });

        request.done(function( msg ) {
          // $( "#log" ).html( msg );
            loader.hide();
            $('#query').val('');
            // console.log(msg)

            var map = new google.maps.Map(document.getElementById('map'), {
                center: new google.maps.LatLng(36.1699, -115.1398),
                zoom: 10
            });
            var infoWindow = new google.maps.InfoWindow;


            msg.forEach(function(markerElem) {
                var name = markerElem['name'];
                var address = markerElem['full_address'];
                // var type = markerElem.getAttribute('type');
                var point = new google.maps.LatLng(
                  parseFloat(markerElem['latitude']),
                  parseFloat(markerElem['longitude']));

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


                var icon = customLabel[0] || {};
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

        request.fail(function( jqXHR, textStatus ) {
            loader.hide();

          alert( "Request failed: " + textStatus );
        });
    });
});

