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


           // container = $('restaurants-container');
            var outer = document.getElementById('restaurants-container');


            // <div class="restaurant">
            //             <div class="row">
            //                 <div class="col-sm-4">
            //                     <div class="row">
            //                         <div class="container">
            //                             <strong>Young Henry's</strong>
            //                         </div>
            //                     </div>
            //                     <div class="row">
            //                         <div class="container restaurant-stars">
            //                             <span class="glyphicon glyphicon-star-empty"></span>
            //                             <span class="glyphicon glyphicon-star-empty"></span>
            //                             <span class="glyphicon glyphicon-star-empty"></span>
            //                             <span class="glyphicon glyphicon-star-empty"></span>
            //                             <span class="glyphicon glyphicon-star-empty"></span>
            //                         </div>
            //                     </div>
            //                 </div>
            //
            //                 <div class="col-sm-8">
            //                     Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Aenean
            // lacinia bibendum nulla
            //                 </div>
            //             </div>
            //         </div>


            msg.forEach(function(markerElem) {
                var name = markerElem['name'];
                var address = markerElem['address'];
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


               var restaurant = document.createElement('div');
               restaurant.setAttribute('class', 'restaurant');

               var row = document.createElement('div');
               row.setAttribute('class', 'row');

               var col_sm4 = document.createElement('div');
               col_sm4.setAttribute('class', 'col-sm-4');

               var inner_row = document.createElement('div');
               inner_row.setAttribute('class', 'row');

               var inner_row2 = document.createElement('div');
               inner_row2.setAttribute('class', 'row');

               var inner_container = document.createElement('div');
               inner_container.setAttribute('class', 'container');

               var inner_container2 = document.createElement('div');
               inner_container2.setAttribute('class', 'container restaurant-stars ');

               inner_container2.appendChild(rating);

               var strong = document.createElement('strong');
               strong.textContent = name;

               var col_sm8 = document.createElement('div');
               col_sm8.setAttribute('class', 'col-sm-8');

               var res_address = document.createElement('text');
               res_address.textContent = address;


           // restaurant.appendChild()
           //  inner_container.appendChild(document.createElement)
           //  inner_row.appendChild(inner_container);

            inner_container.appendChild(strong);
            inner_row.appendChild(inner_container);
            col_sm4.appendChild(inner_row);

            inner_row2.appendChild(inner_container2);
            col_sm4.appendChild(inner_row2);
            row.appendChild(col_sm4);

            col_sm8.appendChild(res_address);
            row.appendChild(col_sm8);
            restaurant.appendChild(row);

            outer.appendChild(restaurant);




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

