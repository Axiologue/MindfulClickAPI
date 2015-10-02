'use strict';

describe('BaseURL service', function() {

  // load modules
  beforeEach(module('cross'));

  // Make sure BaseURL returns a string that starts with http(s)://
  it('should return a string that starts with http(s)://', inject(function(BaseUrl) {
      expect(BaseUrl).toMatch(/^(http|https):\/\//);
    }));

  // and ends with a trailing slash
  it('and end with a /', inject(function(BaseUrl) {
      expect(BaseUrl).toMatch(/\/$/);
    }));
});

describe('Restful service', function () {
  var $httpBackend;
  var $rootScope;

  // load modules
  beforeEach(module('cross'));

  // New matcher to compare only data, not objects
  beforeEach(function() {
    this.addMatchers({
      toEqualData: function(expected) {
        return angular.equals(this.actual, expected);
      }
    })
  });

  // Add mocking tools
  beforeEach(inject(function ($injector) {
    $httpBackend = $injector.get('$httpBackend');
    $rootScope = $injector.get('$rootScope');
  }));

  describe('Article', function () {

  });


});

