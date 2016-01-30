function initialize() {
  
  //Brings out googlemaps after initializing the page
  var mapProp = {
    center:new google.maps.LatLng(37.877742,-97.380979),
    zoom:4,
    mapTypeId:google.maps.MapTypeId.ROADMAP
  };
  var map=new google.maps.Map(document.getElementById("googleMap"),mapProp);
}
google.maps.event.addDomListener(window, 'load', initialize);