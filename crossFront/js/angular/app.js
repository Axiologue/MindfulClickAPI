'use strict';

var cross = angular.module('cross', [
  'crossControllers',
  'crossServices'
]);

cross.config(function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
});