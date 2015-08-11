'use strict';

var cross = angular.module('cross', [
  'crossServices',
  'ngRoute',
  'ngCookies',
  'ngSanitize',
  'ngResource'
]);

cross.config(['$resourceProvider',function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

cross.config(['$routeProvider',
  function($routeProvider) { 
    $routeProvider.
      when('/', {
        templateUrl: 'templates/articles.html',
        controller: 'ArticleCtrl',
        resolve: {
          authenticated: ['djangoAuth', function(djangoAuth){
            // MAKE TRUE FOR PRODUCTION
            return djangoAuth.authenticationStatus();
          }],
        }
      })
      .when('/login', {
        templateUrl: 'templates/auth/login.html',
        resolve: {
          authenticated: ['djangoAuth', function(djangoAuth){
            return djangoAuth.authenticationStatus();
          }],
        }
      })
      .when('/userProfile', {
        templateUrl: 'templates/auth/userprofile.html',
        controller: 'ProfilePageCtrl',
        resolve: {
          authenticated: ['djangoAuth', function(djangoAuth){
            // MAKE TRUE FOR PRODUCTION
            return djangoAuth.authenticationStatus();
          }],
        }
      })
      .when('/signUp', {
        templateUrl: 'templates/auth/signup.html',
        resolve: {
          authenticated: ['djangoAuth', function(djangoAuth){
            // MAKE TRUE FOR PRODUCTION
            return djangoAuth.authenticationStatus();
          }]
        }
      })
      .when('/verifyEmail/:emailVerificationToken', {
        templateUrl: 'templates/auth/verifyemail.html',
        resolve: {
          authenticated: ['djangoAuth', function(djangoAuth){
            return djangoAuth.authenticationStatus();
          }],
        }
      })
      .when('/passwordReset', {
        templateUrl: 'templates/auth/passwordreset.html',
        resolve: {
          authenticated: ['djangoAuth', function(djangoAuth){
            return djangoAuth.authenticationStatus();
          }],
        }
      })
      .when('/passwordResetConfirm/:firstToken/:passwordResetToken', {
        templateUrl: 'templates/auth/passwordresetconfirm.html',
        resolve: {
          authenticated: ['djangoAuth', function(djangoAuth){
            return djangoAuth.authenticationStatus();
          }],
        }
      })
      .otherwise({
        redirectTo: '/'
      });
}]);