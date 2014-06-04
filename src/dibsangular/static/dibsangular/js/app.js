

// Declare app level module which depends on filters, and services
angular.module('dibsApp', [
  'ngRoute',
  'ngCookies',
  'dibsApp.filters',
  'dibsApp.services',
  'dibsApp.directives',
  'dibsApp.controllers'
]).
config(['$routeProvider', function($routeProvider) {
  'use strict';
  /* TODO: somehow inject '/static/' */
  $routeProvider.when('/list', {templateUrl: '/static/dibsangular/partials/list.html', controller: 'ListCtrl'});
  $routeProvider.when('/view2', {templateUrl: '/static/dibsangular/partials/partial2.html', controller: 'MyCtrl2'});
  $routeProvider.otherwise({redirectTo: '/view1'});
}]).config(['$httpProvider', function($httpProvider) {
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
}]);

