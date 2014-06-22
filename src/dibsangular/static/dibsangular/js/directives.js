/* Directives */

var dibs_messages = {
    'UNLOCK_NOPERM': "You can't unlock this item",
    'LOCK_NOPERM': "You can't lock this item",
};

////////////////////////////////////////////////////////////////////////////////

var dibs_directives = angular.module('dibsApp.directives', []);

////////////////////////////////////////////////////////////////////////////////

dibs_directives.directive('dibsItemList', function() {
  return {
    'restrict': 'E',
    'scope': {
      'items': '='
    },
    'templateUrl': '/static/dibsangular/partials/list.html',
    'controller': function($scope, $http, $log) {

      $http.get('/api/v1/items/').success(function(data) {
        $scope.items = data;
      });
    }
  };
});

////////////////////////////////////////////////////////////////////////////////

dibs_directives.directive('dibsItem', function() {

    return {
      'restrict': 'E',
      'scope': {
        'item': '='
      },
      'templateUrl': '/static/dibsangular/partials/detail.html',
      'controller': ItemController
    };
  });

////////////////////////////////////////////////////////////////////////////////

var ItemController = function($scope, $http, $log, sse) {

  $scope.item.errors = [];

  $scope.refresh = function(item) {
    $http.get(item.url).success(function(data){
      var item = data;
      $scope.item = item;
    });
  };

  sse.addEventListener('itemChange', function (e) {
    if (e.data === $scope.item.id.toString()) {
        $scope.refresh($scope.item);
    }
  });

  $scope.lock = function (item) {
    $http.post(item.url + 'lock/').
      success(function(data) {
        $log.debug(data);
        $scope.refresh(item);
      }).
      error(function(data, status, headers, config) {
        $log.error(status);
        $log.error(data);
        if (status === 403) {
          $scope.item.errors.push(dibs_messages.LOCK_NOPERM);
        }
      });
  };

  $scope.unlock = function (item) {
    $http.post(item.url + 'unlock/').
      success(function(data) {
        $log.debug(data);
        $scope.refresh(item);
      }).
      error(function(data, status, headers, config) {
        $log.error(status);
        $log.error(data);
        if (status === 403) {
          $scope.item.errors.push(dibs_messages.UNLOCK_NOPERM);
        }
    });
  };

  $scope.closeAlert = function(index) {
    $scope.item.errors.splice(index, 1);
  };
};

////////////////////////////////////////////////////////////////////////////////

dibs_directives.directive('appVersion', ['version', function(version) {
  return function(scope, elm, attrs) {
    elm.text(version);
  };
}]);
