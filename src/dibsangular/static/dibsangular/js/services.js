/* Services */
var dibs_version = '0.1.0-dev';

var dibs_messages = {
    'UNLOCK_NOPERM': "You can't unlock this item",
    'LOCK_NOPERM': "You can't lock this item",
};

// Demonstrate how to register services
// In this case it is a simple value service.
var dibs_services = angular.module('dibsApp.services', []);

dibs_services.value('version', dibs_version);
dibs_services.value('dibs_messages', dibs_messages);

dibs_services.factory('sse', function($rootScope) {
  var sse = new EventSource('/stream');
  return {
    addEventListener: function(eventName, callback) {
      sse.addEventListener(eventName, function() {
        var args = arguments;
        $rootScope.$apply(function () {
          callback.apply(sse, args);
        });
      });
    }
  };
});
