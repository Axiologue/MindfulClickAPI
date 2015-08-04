'use strict';

var cross = angular.module('cross', [
  'crossControllers',
  'crossServices'
]);

cross.config(['$resourceProvider',function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);