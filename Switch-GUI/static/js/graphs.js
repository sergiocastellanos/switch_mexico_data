
//Function to get the data and the execute the map renderization
queue(2)
    .defer(d3.json, "/nodes")
    .defer(d3.json, "/node2")
    .await(makeMap);

// function to render the map
function makeMap(error, node1,node2){


      var node1 =  node1;
      alert(node1);
      alert(node2);

      var map = L.map('map');

  var drawMap = function(){
    map.setView([23,-105], 13);
    mapLink = '<a href="http://openstreetmap.org">OpenStreetMap</a>';
    L.tileLayer(
      'http://{s}.tile.openstreetmap.se/hydda/base/{z}/{x}/{y}.png', {
        attribution: '&copy; ' + mapLink + ' Contributors',
        maxZoom: 5,
      }).addTo(map);

    var e =  L.geoJson(node1).addTo(map).bindPopup('Some information');
};

//Draw Map
drawMap();

}
