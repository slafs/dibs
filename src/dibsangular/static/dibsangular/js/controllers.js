
/* Controllers */

angular.module('dibsApp.controllers', []).
  controller('ListCtrl', function($scope, $http, $log) {
    'use strict';

    $scope.items = [];

    /* sets a given item in scope */
    var set_item = function(item) {
      $log.debug("set_item");
      $log.debug(item);
      for (var i = 0; i < $scope.items.length; i++) {
        $log.debug($scope.items[i]);
        if ($scope.items[i].id === item.id) {
          $log.debug("found");
          $scope.items[i] = item;
          break;
        }
      }
    };

    $http.get('/api/v1/items/').success(function(data) {
      $scope.items = data;
    });

  // }).controller

    $scope.refresh = function(item) {
      $http.get(item.url).success(function(data){
        var item = data;
        set_item(item);
      });
    };

    $scope.lock = function (item) {
        $http.post(item.url + 'lock/').success(function(data) {
          $log.debug(data);
          $scope.refresh(item);
        });
    };
    $scope.unlock = function (item) {
        $http.post(item.url + 'unlock/').success(function(data) {
          $log.debug(data);
          $scope.refresh(item);
        });
    };

  })
  .controller('MyCtrl2', [function() {

  }]);
