var crossServices = angular.module('crossServices',['ngResource']);

// use for setting the API endpoint location
crossServices.factory('BaseUrl', [function () {
  var baseUrl = 'http://localhost:8000/'

  return baseUrl;
}]);

// For making Article-related API calls
crossServices.factory('Article',['$resource', 'BaseUrl',
  function ($resource, BaseUrl){
    return $resource(BaseUrl + 'articles/articles/:articleID/', {}, {
      query: {method:'GET', params:{articleID:'untagged'}, isArray:true},
      queryTagged: {method:'GET', params:{articleID:'tagged'}, isArray:true},
      update: {method: 'PUT'}
  });
}]);

// For making tag-related API calls
crossServices.factory('eTag',['$resource', 'BaseUrl',
  function ($resource, BaseUrl) {
    return $resource(BaseUrl + 'tags/etags/:tagID/',{},{
      query: {method:'GET',params:{tagID:'list'},isArray:true},
      update: {method: 'PUT'}
    });
}]);

// For getting company and ethics lists, used in form-making
crossServices.factory('Meta',['$resource', 'BaseUrl',
  function ($resource, BaseUrl) {
    return $resource(BaseUrl + 'tags/formMeta/',{},{
      query: {method:'GET',params:{},isArray:true},
    });
}]);

// For managing Tag Types
crossServices.factory('eType',['$resource', 'BaseUrl',
  function ($resource, BaseUrl) {
    return $resource(BaseUrl + 'tags/etypes/:tagTypeID/',{},{
      save: {method:'POST',params:{tagTypeID:'new'}},
    });
}]);
