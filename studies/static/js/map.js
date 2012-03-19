google.load('jquery', '1.7.1');
google.load('maps', '3.x', {"other_params": "sensor=false"});

function loadLibraries() {
    var libs = [
        "/static/js/markerclusterer.js",
        // "/media/js/TimeControl.js",
    ];
    var libsLength = libs.length;
    for (i=0; i<libsLength; i++) {
        var lib = libs[i];
        var counter = libsLength;
        $.getScript(lib, function(code) {
            counter--;
            if (counter == 0) {
                initialize();
            }
        });
    }
}


function initialize() {
    var directionsDisplay;
    var map;
    var oldDirections = [];
    var currentDirections = null;
    var mapOptions = {
      zoom: 12,
      center: new google.maps.LatLng(-28.643387, 153.612224),
      mapTypeId: google.maps.MapTypeId.ROADMAP,
      mapTypeControl: true,
      mapTypeControlOptions: {
          style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
          position: google.maps.ControlPosition.RIGHT_BOTTOM
      },
      panControl: false,
      panControlOptions: {
          position: google.maps.ControlPosition.TOP_RIGHT
      },
      zoomControl: false,
      zoomControlOptions: {
          style: google.maps.ZoomControlStyle.LARGE,
          position: google.maps.ControlPosition.LEFT_CENTER
      },
      scaleControl: false,
      scaleControlOptions: {
          position: google.maps.ControlPosition.TOP_LEFT
      },
      streetViewControl: false,
      streetViewControlOptions: {
          position: google.maps.ControlPosition.LEFT_TOP
      }
    }
    map = new google.maps.Map(document.getElementById("map"), mapOptions);

    $("#toggleKeyboard").click(function(e) {
        $("#phoneticKeyboard").toggle();
        return false;
    });
    var form = $("#searchForm");
    var resultsCount = 1;
    form.submit(function (e) {
        var self = $(this);
        var values = decodeURIComponent(self.serialize());
        var data = {
            q: $("#id_q").val().trim(),
            match: $("#id_match").val().trim(),
            where: $("#id_where").val().trim(),
            study: $("#id_study").val().trim(),
            id: resultsCount
        };
        resultsCount += 1;
        if (data.q != "") {
            $.ajax({
                url: "/map/",
                dataType: "json",
                processData: true,
                type: "GET",
                contentType: " application/x-www-form-urlencoded",
                mimeType: "application/json",
                data: data,
//                success: function(result) {
//                    console.log(result);
//                    $(".well").show();
//                    var p = $("<P>");
//                    var pId = "results-"+ resultsCount;
//                    data["id"] = pId;
//                    p.attr("id", pId)
//                    p.attr("class", "color-"+ resultsCount);
//                    p.text(pId +":"+ values);
//                    $(".well").prepend(p)
//                },
                success: function(data){
                   console.log( "Data: " + JSON.stringify(data) );
                },
                error:function (jqXHR, textStatus, errorThrown){
                   console.log(JSON.stringify(jqXHR) + ' ' + textStatus +'  '+errorThrown );
                }
            });
            
        }
        return false;
    });
}


//    var markers = [];
//    var polygons = [];
//    var map = new google.maps.Map(document.getElementById('map'));
////    var markerClusterer = new MarkerClusterer(map, markers, {maxZoom: 10});
////    map.addControl(new google.maps.LargeMapControl3D());
////    map.addMapType(google.maps.PHYSICAL_MAP);
////    var hierarchyControl = new google.maps.HierarchicalMapTypeControl();
////    hierarchyControl.addRelationship(google.maps.SATELLITE_MAP, google.maps.HYBRID_MAP, null, false);
////    map.addControl(hierarchyControl);
////    map.setMapType(google.maps.PHYSICAL_MAP);
//    var center;
//    // Centered at client location with zoom level 3
//    // Try W3C Geolocation (Preferred)
//    if (navigator.geolocation) {
//        browserSupportFlag = true;
//        navigator.geolocation.getCurrentPosition(function(position) {
//            center = new google.maps.LatLng(position.coords.latitude,
//                                            position.coords.longitude);
//            map.setCenter(center, 4);
//        }, function() {
//            // Try Google ClientLocation
//            if (google.loader.ClientLocation) {
//                center = new google.maps.LatLng(google.loader.ClientLocation.latitude,
//                                                google.loader.ClientLocation.longitude);
//            // Set middle of the Atlantic Ocean
//            } else {
//                center = new google.maps.LatLng(26.9, -35.5);
//            }
//            map.setCenter(center, 4);
//        });
//    }
////    map.enableDragging();
////    map.enableScrollWheelZoom();
//    $(window).unload(function() {
//        google.maps.Unload();
//    });

//    function drawClusters(data) {
//        if (markerClusterer && markerClusterer.clearMarkers) {
//            markerClusterer.clearMarkers();
//        }
//        markers = [];
//        polygons = [];
//        map.clearOverlays();
//        $("#progress").progressbar('value', 1);
//        var parentMap = map;
//        var factor = (100-2) / data.length;
//        for(i=0; i<data.length; i++) {
//            var item = data[i];
//            if (parseInt(i*factor) != parseInt((i-1)*factor)) {
//                $("#progress").progressbar('value', parseInt(i*factor));
//            }
//            if (item.coordinates) {
//                var geometry = getGeometryFromWKT(item.coordinates, item.geometry, item.place);
//                if (geometry instanceof google.maps.Marker) {
//                    var parentItem = item;
//                    geometry.identifier = item.identifier;
//                    geometry.place = item.place;
//                    google.maps.Event.addListener(geometry, "click", function(e) {
//                        var url = "/artworks/locations/"+ this.identifier +"/list/";
//                        var parentMarker = this;
//                        $.getJSON(url, {"type": artworkPlaceFilter}, function(json_data) {
//                            var html = "";
//                            for(var j=0; j<json_data.length; j++) {
//                                var elto = json_data[j];
//                                html += "<li><a href='"+ elto.url +"'>"+ elto.title +"</a> ("+ elto.creators +")</li>";
//                            }
//                            parentMarker.openInfoWindowHtml(
//                                "<span class='infoWindow'><div class='artworkTitle'>"+ parentMarker.place +" ["+ json_data.length +"]</div><div class='artworkList'><ol>"+ html +"</ol></div></span>"
//                            , {maxHeight: 150, maxWidth: 500});
//                        });
//                    });
//                    markers.push(geometry);
//                }
//            }
//        }
//        markerClusterer.addMarkers(markers);
//        $("#progress").hide();
//    }

//    function getGeometryFromWKT(wkt_point, wkt_geometry, title) {
//        multipolygonRegExp = /^MULTIPOLYGON\s*\(\(\((([+-]?\d+(\.\d+)? [+-]?\d+(\.\d+)?,\s*)+([+-]?\d+(\.\d+)? [+-]?\d+(\.\d+)?){1})\)\)(,\s*\(\((([+-]?\d+(\.\d+)? [+-]?\d+(\.\d+)?,\s*)+([+-]?\d+(\.\d+)? [+-]?\d+(\.\d+)?){1})\)\))*\)$/;
//        multipolygonMatch = wkt_geometry.match(multipolygonRegExp);
//        polygonRegExp = /^POLYGON\s*\(\((([+-]?\d+(\.\d+)? [+-]?\d+(\.\d+)?,\s*)+([+-]?\d+(\.\d+)? [+-]?\d+(\.\d+)?){1})\)\)$/;
//        polygonMatch = wkt_geometry.match(polygonRegExp);
//        pointRegExp = /^POINT\s*\(([+-]?\d+(\.\d+)? [+-]?\d+(\.\d+)?){1}\)$/;
//        pointMatch = wkt_point.match(pointRegExp);
//        if (multipolygonMatch || polygonMatch) {
//            if (multipolygonMatch) {
//                polygonsList = wkt_geometry.split(/MULTIPOLYGON\s*\(\s*\(\s*\(\s*(.*)\s*\)\s*\)\s*\)/i)[1].split(/\s*\)\s*\)\s*,\s*\(\s*\(\s*/);
//            } else {
//                polygonsList = [polygonMatch[1]];
//            }
//            var polygonsObjects = [];
//            for(var p=0; p<polygonsList.length; p++) {
//                var polygonString = polygonsList[p];
//                var points = [];
//                var wktPoints = polygonString.split(", ");
//                for(var i=0; i<wktPoints.length; i++) {
//                    var wktPoint = wktPoints[i].split(" ");
//                    var point = new google.maps.LatLng(wktPoint[1], wktPoint[0]);
//                    points.push(point);
//                }
//                polygonsObjects[polygonsObjects.length] = new google.maps.Polygon(points, "#FF8000", 2, undefined, "#FF8000", 0.25);
//            }
//        }
//        if (pointMatch) {
//            var wktPoint = pointMatch[1].split(" ");
//            var point = new google.maps.LatLng(wktPoint[1], wktPoint[0]);
//            var marker, markerOptions;
//            if (multipolygonMatch || polygonMatch) {
//                markerOptions = {
//                    icon: markerWorld,
//                    title: title
//                }
//                marker = new google.maps.Marker(point, markerOptions);
//                google.maps.Event.addListener(marker, "mouseover", function(e) {
//                    var parentMarker = this;
//                    for(var ig=0; ig<polygonsObjects.length; ig++) {
//                        var polygon = polygonsObjects[ig];
//                        map.addOverlay(polygon);
//                    }
//                });
//                google.maps.Event.addListener(marker, "mouseout", function(e) {
//                    var parentMarker = this;
//                    for(var ig=0; ig<polygonsObjects.length; ig++) {
//                        var polygon = polygonsObjects[ig];
//                        map.removeOverlay(polygon);
//                    }
//                });
//            } else {
//                markerOptions = {
//                    icon: markerArtwork,
//                    title: title
//                }
//                marker = new google.maps.Marker(point, markerOptions);
//            }
//            return marker;
//        }
//    }

google.setOnLoadCallback(loadLibraries);
