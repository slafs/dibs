
/* Controllers */

angular.module('dibsApp.controllers', []).
  controller('ListCtrl', function($scope, $http) {
    'use strict';

    $http.get('/api/v1/items/').success(function(data) {
      $scope.items = data;
    });

    $scope.lock = function (item) {
        $http.post(item.url + 'lock/').success(function(data) {
          console.log("post OK", data);
        });
        console.log("locking", item);
        item.locked_by = 'mua';
    };

  })
  .controller('MyCtrl2', [function() {

  }]);

