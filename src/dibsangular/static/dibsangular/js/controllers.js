
/* Controllers */

var dibs_controllers = angular.module('dibsApp.controllers', []);

dibs_controllers.controller('ListCtrl', function($scope, $http, $log) {
  $scope.items = null;
});


dibs_controllers.controller('NavCtrl', function($scope) {
    $scope.navbarCollapsed = true;
});
