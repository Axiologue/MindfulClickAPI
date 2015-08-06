'use strict';

describe('Cross app', function () {
  it('Should show the web page', function () {
    browser.get('/');
    expect(element(by.css('.crossList.row h1')).getText()).toBe('Analyzed Articles');
  })
});