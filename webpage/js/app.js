(function() {
    "use strict";

    angular
        .module("pollMain", ["ngRoute", "pollControllers"])
        .config(routing);

    routing.$inject  = ["$routeProvider"];
    function routing($routeProvider) {
        $routeProvider
        .when("/", {
            templateUrl: "partials/landing.html",
            controller: "LandingCtrl",
            controllerAs: "vm"
        })
        .when("/history", {
            templateUrl: "partials/history.html",
            controller: "MapCtrl",
            controllerAs: "vm"
        })
        .when("/info", {
            templateUrl: "partials/info.html",
            controller: "MapCtrl",
            controllerAs: "vm"
        })
        .otherwise({
            redirectTo: "/"
        });
    }
})();
