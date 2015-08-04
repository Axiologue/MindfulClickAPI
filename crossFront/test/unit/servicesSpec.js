'use strict';

describe('service', function() {

  // load modules
  beforeEach(module('cross'));

  // Make sure BaseURL returns a string that starts with http(s)://
  it('ensure BaseUrl returns http string', inject(function(BaseUrl) {
      expect(BaseUrl).toMatch(/^(http|https):\/\//);
    }));
});