var crossServices = angular.module('crossServices',['ngResource']);

crossServices.factory('Article',['$resource',
  function ($resource){
    return $resource('http://localhost:8000/cross/articles/:articleID/', {}, {
      query: {method:'GET', params:{articleID:'all'}, isArray:true},
      update: {method: 'PUT'}
  });
}]);

crossServices.factory('Cross',['$resource',
  function ($resource) {
    return $resource('http://localhost:8000/cross/cross/:crossID/',{},{
      query: {method:'GET',params:{crossID:'list'},isArray:true},
      update: {method: 'PUT'}
    });
}]);