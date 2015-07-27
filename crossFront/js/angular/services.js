var crossServices = angular.module('crossServices',['ngResource']);

crossServices.factory('Article',['$resource',
  function ($resource){
    return $resource('http://api.axiologue.org/cross/articles/:articleID/', {}, {
      query: {method:'GET', params:{articleID:'all'}, isArray:true},
      update: {method: 'PUT'}
  });
}]);

crossServices.factory('Cross',['$resource',
  function ($resource) {
    return $resource('http://api.axiologue.org/cross/cross/:crossID/',{},{
      query: {method:'GET',params:{crossID:'list'},isArray:true},
      update: {method: 'PUT'}
    });
}]);

crossServices.factory('Meta',['$resource',
  function ($resource) {
    return $resource('http://api.axiologue.org/cross/formMeta',{},{
      query: {method:'GET',params:{crossID:'list'},isArray:true},
    });
}]);