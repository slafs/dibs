'use strict';

/* Controllers */

angular.module('dibsApp.controllers', []).
  controller('ListCtrl', function($scope) {
    $scope.items = [
        {name: "Element1", desc: "Some description", locked_by: null},
        {name: "Element2", desc: "Some other description", locked_by: 'testuser'},
    ];
  })
  .controller('MyCtrl2', [function() {

  }]);
