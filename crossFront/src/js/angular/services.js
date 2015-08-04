var crossServices = angular.module('crossServices',['ngResource']);

// use for setting the API endpoint location
crossServices.factory('BaseUrl', [function () {
  var baseUrl = 'http://api.axiologue.org/';

  return baseUrl;
}]);

// For making Article-related API calls
crossServices.factory('Article',['$resource', 'BaseUrl',
  function ($resource, BaseUrl){
    return $resource(BaseUrl + 'cross/articles/:articleID/', {}, {
      query: {method:'GET', params:{articleID:'all'}, isArray:true},
      update: {method: 'PUT'}
  });
}]);

// For making tag-related API calls
crossServices.factory('Cross',['$resource', 'BaseUrl',
  function ($resource, BaseUrl) {
    return $resource(BaseUrl + 'cross/cross/:crossID/',{},{
      query: {method:'GET',params:{crossID:'list'},isArray:true},
      update: {method: 'PUT'}
    });
}]);

// For getting company and ethics lists, used in form-making
crossServices.factory('Meta',['$resource', 'BaseUrl',
  function ($resource, BaseUrl) {
    return $resource(BaseUrl + 'cross/formMeta',{},{
      query: {method:'GET',params:{crossID:'list'},isArray:true},
    });
}]);