google.load('jquery', '1.7.1');
google.load('maps', '3.x', {"other_params": "sensor=false"});

function loadLibraries() {
    var libs = [
        "/static/js/markerclusterer.js",
        "/static/js/jquery.haschange.min.js"
        // "/media/js/TimeControl.js",
    ];
    var libsLength = libs.length;
    for (i=0; i<libsLength; i++) {
        var lib = libs[i];
        var counter = libsLength;
        $.getScript(lib, function(code) {
            counter--;
            if (counter == 0) {
                main();
            }
        });
    }
}

function main() {
    (function ($) {
        $(document).ready(initialize);
        function initialize() {
            var map;
            var searches = [];
            var polygonSet = {};
            var recentSearches = [];
            var resultsCount = 1;
            $(window).hashchange(hashchange);
            $(window).hashchange();

            function hashchange() {
                var hash, paramsList, length;
                hash = location.hash.substring(1);
                if (hash) {
                    if (map) {
                        // map.clear();
                    }
                    searches = [];
                    polygonSet = {};
                    recentSearches = [];
                    $("#searchs").html("");
                    paramsList = JSON.parse(hash);
                    length = paramsList.length;
                    for(i=0; i < length; i++) {
                        addSearch(paramsList[i]);
                    }
                    location.hash = "";
                }
            };

            var mapOptions = {
              zoom: 3,
              center: new google.maps.LatLng(30.751873645557307, -40.417622248316455),
              mapTypeId: google.maps.MapTypeId.TERRAIN,
              mapTypeControl: true,
              mapTypeControlOptions: {
                  style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
                  position: google.maps.ControlPosition.RIGHT_BOTTOM
              },
              panControl: true,
              panControlOptions: {
                  position: google.maps.ControlPosition.LEFT_CENTER
              },
              zoomControl: true,
              zoomControlOptions: {
                  style: google.maps.ZoomControlStyle.SMALL,
                  position: google.maps.ControlPosition.LEFT_CENTER
              },
              scaleControl: true,
              scaleControlOptions: {
                  position: google.maps.ControlPosition.LEFT_BOTTOM
              },
              streetViewControl: false,
              streetViewControlOptions: {
                  position: google.maps.ControlPosition.LEFT_TOP
              }
            }
            map = new google.maps.Map(document.getElementById("map"), mapOptions);
            var form = $("#searchForm");
            $("#searchForm").submit(function(e) {
                // var key, values = decodeURIComponent(form.serialize());
                var params = {
                    q: $("#id_q").val().trim(),
                    match: $("#id_match").val().trim(),
                    where: $("#id_where").val().trim(),
                    study: $("#id_study").val().trim(),
                    id: resultsCount
                };
                addSearch(params);
                return false;
            });

            function addSearch(params) {
                label = function(item) {
                    var output = "";
                    output += $("label[for='id_"+ item +"']").text();
                    output += " ";
                    output += $("#id_"+ item).find("option[value='"+ params[item] +"']").text();
                    return output;
                }
                var text = label("match") +" "+  label("where") +" "+ label("study");
                $(".well").show();
                var anchor = $("<a>");
                var spanSquare = $("<SPAN>");
                spanSquare.addClass("resultSquare").addClass("bgolor-"+ resultsCount);
                var spanText = $("<SPAN>");
                spanText.text(text);
                spanText.addClass("resultText");
                var spanQ = $("<SPAN>");
                spanQ.text(params.q);
                spanQ.addClass("resultQuery");
                var spanResults = $("<SPAN>");
                spanResults.text("Loading...");
                spanResults.attr("id", "results-"+ resultsCount +"-results")
                spanResults.addClass("resultTotal");
                var pId = "results-"+ resultsCount;
                anchor.attr("id", pId);
                anchor.attr("href", "javascript:void(0);");
                anchor.addClass("resultRow");
                anchor.addClass("resultDisabled");
                anchor.append(spanSquare);
                anchor.append(spanQ)
                anchor.append(spanResults);
                anchor.append(spanText);
                resultsCount += 1;
                key = params.q + params.match + params.where + params.study;
                if ((params.q != "") && (recentSearches.indexOf(key) < 0)) {
                    recentSearches.push(key);
                    searches.push(params)
                    $("#link").val(location.origin + location.pathname +"#"+ JSON.stringify(searches));
                    $("#searchs").prepend(anchor);
                    $.ajax({
                        url: "/map/",
                        dataType: "json",
                        processData: true,
                        type: "GET",
                        data: params,
                        success: function(data, textStatus, jqXHR) {
                            $("#results-"+ data.id).click(function() {
                                var self = $(this);
                                if (self.hasClass("resultDisabled")) {
                                    for(i=0; i<polygonSet[data.id].length; i++) {
                                        polygonSet[data.id][i].setMap(map);
                                    }
                                    self.removeClass("resultDisabled");
                                } else {
                                    for(i=0; i<polygonSet[data.id].length; i++) {
                                        polygonSet[data.id][i].setMap(null);
                                    }
                                    self.addClass("resultDisabled");
                                }
                            });
                            var result = $("#results-"+ data.id +"-results");
                            if (data.places) {
                                result.text("("+ data.places.length +" places, "+ data.total +" productions)");
                                if (!polygonSet[data.id]) {
                                    polygonSet[data.id] = [];
                                }
                                var polygons = getGeometryFromWKT(data.centroid, data.boundaries, params.q, colors[data.id]);
                                polygonSet[data.id] = polygonSet[data.id].concat(polygons);
                                for(i=0; i<data.places.length; i++) {
                                    var place = data.places[i];
                                    var polygons = getGeometryFromWKT(place.point, place.geometry, place.title, colors[data.id], true);
                                    polygonSet[data.id] = polygonSet[data.id].concat(polygons);
                                }
                            } else {
                                result.text("(No places, no productions)");
                            }
                            $("#results-"+ data.id).click();
                            $("#toggleResults").css("display", "inline");
                        },
                        error: function(jqXHR, textStatus, errorThrown) {
                           console.log(JSON.stringify(jqXHR) +' '+ textStatus +'  '+ errorThrown );
                        }
                    });
                }
            };

            function getGeometryFromWKT(wkt_point, wkt_geometry, title, color, isSubPolygon) {
                multipolygonRegExp = /^MULTIPOLYGON\s*\(\(\((([+-]?\d+(\.\d+)? [+-]?\d+(\.\d+)?,\s*)+([+-]?\d+(\.\d+)? [+-]?\d+(\.\d+)?){1})\)\)(,\s*\(\((([+-]?\d+(\.\d+)? [+-]?\d+(\.\d+)?,\s*)+([+-]?\d+(\.\d+)? [+-]?\d+(\.\d+)?){1})\)\))*\)$/;
                multipolygonMatch = wkt_geometry.match(multipolygonRegExp);
                polygonRegExp = /^POLYGON\s*\(\((([+-]?\d+(\.\d+)? [+-]?\d+(\.\d+)?,\s*)+([+-]?\d+(\.\d+)? [+-]?\d+(\.\d+)?){1})\)\)$/;
                polygonMatch = wkt_geometry.match(polygonRegExp);
                pointRegExp = /^POINT\s*\(([+-]?\d+(\.\d+)? [+-]?\d+(\.\d+)?){1}\)$/;
                pointMatch = wkt_point.match(pointRegExp);
                if (multipolygonMatch || polygonMatch) {
                    if (multipolygonMatch) {
                        polygonsList = wkt_geometry.split(/MULTIPOLYGON\s*\(\s*\(\s*\(\s*(.*)\s*\)\s*\)\s*\)/i)[1].split(/\s*\)\s*\)\s*,\s*\(\s*\(\s*/);
                    } else {
                        polygonsList = [polygonMatch[1]];
                    }
                    var polygonsObjects = [];
                    for(var p=0; p<polygonsList.length; p++) {
                        var polygonString = polygonsList[p];
                        var points = [];
                        var wktPoints = polygonString.split(", ");
                        for(var i=0; i<wktPoints.length; i++) {
                            var wktPoint = wktPoints[i].split(" ");
                            var point = new google.maps.LatLng(wktPoint[1], wktPoint[0]);
                            points.push(point);
                        }
                        var polygonsOptions, polygonsObject;
                        if (isSubPolygon) {
                            polygonsOptions = {
                                paths: points,
                                strokeColor: color,
                                strokeOpacity: 0,
                                strokeWeight: 3,
                                fillColor: color,
                                fillOpacity: 0
                            }
                            polygonsObject = new google.maps.Polygon(polygonsOptions);
                            google.maps.event.addListener(polygonsObject, 'mouseover', function() {
                                this.setOptions({strokeOpacity: 0.8});
                            });
                            google.maps.event.addListener(polygonsObject, 'mouseout', function() {
                                this.setOptions({strokeOpacity: 0});
                            });
                        } else {
                            polygonsOptions = {
                                paths: points,
                                strokeColor: color,
                                strokeOpacity: 0.8,
                                strokeWeight: 2,
                                fillColor: color,
                                fillOpacity: 0.25
                            }
                            polygonsObject = new google.maps.Polygon(polygonsOptions);
                        }
                        polygonsObjects[polygonsObjects.length] = polygonsObject;
                    }
                }
                return polygonsObjects;
            }

            $("#toggleResults").click(function(e) {
                $(".well").toggle();
            });
        }
    })(jQuery);
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
