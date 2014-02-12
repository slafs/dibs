'use strict';

/* Services */
var dibs_version = '0.1.0';

// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('dibsApp.services', []).
  value('version', dibs_version);
