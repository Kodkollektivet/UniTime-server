angular.module('unitime', [
    'ngResource',
    'ngRoute',
    'ngCookies',
    'unitime.services',
    'unitime.controllers',
])

    .config(
    function ($interpolateProvider, $httpProvider, $resourceProvider){


        // Force angular to use square brackets for template tag
        // The alternative is using {% verbatim %}
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');

        // CSRF Support
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

        // This only works in angular 3!
        // It makes dealing with Django slashes at the end of everything easier.
        $resourceProvider.defaults.stripTrailingSlashes = false;

        // Django expects jQuery like headers
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';


        //$locationProvider.html5Mode(false).hashPrefix('!');
});