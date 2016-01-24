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
        .otherwise({
            redirectTo: "/404.html"
        });
    }
})();
