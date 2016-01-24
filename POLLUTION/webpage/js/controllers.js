(function() {
    "use strict";

    angular.module("pollControllers", [])
        .controller("LandingCtrl", LandingCtrl);

    // LandingCtrl.$inject = [""];
    function LandingCtrl() {
        var vm = this;
        vm.test = "HELLO WORLD";
    }
})();
