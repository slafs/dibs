/* Directives */


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

var dibsItemBaseDirective = function() {

    return {
      'restrict': 'E',
      'scope': {'item': '='},
      'controller': ItemController
    };
};

dibs_directives.directive('dibsItem', function() {
  ret_obj = dibsItemBaseDirective();
  ret_obj.templateUrl = '/static/dibsangular/partials/detail.html';
  return ret_obj;
});

////////////////////////////////////////////////////////////////////////////////

var ItemController = function($scope, $http, $log, sse, dibs_messages) {

  $scope.item.errors = [];

  $scope.refresh = function() {
    $http.get($scope.item.url).success(function(data){
      var item = data;

      $scope.item.name = item.name;
      $scope.item.desc = item.desc;
      $scope.item.locked_by = item.locked_by;
      $scope.item.can_be_locked = item.can_be_locked;
      $scope.item.created = item.created;
      $scope.item.modified = item.modified;

      $scope.item.errors = [];
    });
  };

  sse.addEventListener('itemChange', function (e) {
    if (e.data === $scope.item.id.toString()) {
        $scope.refresh();
    }
  });

  $scope.lock = function () {
    $http.post($scope.item.url + 'lock/').
      success(function(data) {
        $log.debug(data);
        $scope.refresh();
      }).
      error(function(data, status, headers, config) {
        $log.error(status);
        $log.error(data);
        if (status === 403) {
          $scope.item.errors.push(dibs_messages.LOCK_NOPERM);
        }
      });
  };

  $scope.unlock = function () {
    $http.post($scope.item.url + 'unlock/').
      success(function(data) {
        $log.debug(data);
        $scope.refresh();
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
