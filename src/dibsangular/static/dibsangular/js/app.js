'use strict';


// Declare app level module which depends on filters, and services
angular.module('dibsApp', [
  'ngRoute',
  'dibsApp.filters',
  'dibsApp.services',
  'dibsApp.directives',
  'dibsApp.controllers'
]).
config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/view1', {templateUrl: '/static/dibsangular/partials/partial1.html', controller: 'MyCtrl1'});
  $routeProvider.when('/view2', {templateUrl: '/static/dibsangular/partials/partial2.html', controller: 'MyCtrl2'});
  $routeProvider.otherwise({redirectTo: '/view1'});
}]);
