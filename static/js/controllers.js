(function() {
    "use strict";

    angular.module("pollControllers", [])
        .controller("LandingCtrl", LandingCtrl)
        .controller("MapCtrl", MapCtrl);

    LandingCtrl.$inject = ["$http"];
    function LandingCtrl($http) {
        var vm = this;
        vm.test = "HELLO WORLD";
        $http.get("LAT_LNG.json").success(function(data) {
            vm.test = "recieved";
            console.log(data);
            vm.data = data;
        });
    }

    function MapCtrl() {
        var vm = this;
        vm.initialize = function() {
            vm.mapOptions = {
                zoom: 8,
                center: new google.maps.LatLng(22.649907498685803, 88.36255413913727)
            };
            vm.map = new google.maps.Map(document.getElementById('googleMap'), vm.mapOptions);
        }

        vm.loadScript = function() {
            console.log("HASDFS");
            var script = document.createElement('script');
            script.type = 'text/javascript';
            script.src = 'https://maps.google.com/maps/api/js?sensor=false&callback=initialize';
            document.body.appendChild(script);
            setTimeout(function() {
                vm.initialize();
            }, 500);
        }
        // vm.mapOptions = {
        //     zoom: 4,
        //     center: new google.maps.LatLng(41.923, 12.513),
        //     mapTypeId: google.maps.MapTypeId.TERRAIN
        // }
        // vm.map = new google.maps.Map(document.getElementById('googleMap'), $scope.mapOptions);
    }

})();
