/* Services */
var dibs_version = '0.1.0';

// Demonstrate how to register services
// In this case it is a simple value service.
var dibs_services = angular.module('dibsApp.services', []);

dibs_services.value('version', dibs_version);
