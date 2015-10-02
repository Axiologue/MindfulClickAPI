'use strict';

angular.module('cross')
.controller('BodyCtrl',['$scope','djangoAuth','$location','$cookies',function ($scope,djangoAuth,$location,$cookies) {
  // Variable to hold the cookie expiration date, which is currently set to one day
  var expires = {};


  // Assume user is not logged in until we hear otherwise
  $scope.authenticated = false;
  // Wait for the status of authentication, set scope var to true if it resolves
  $scope.user = {'username':'','first_name':'','last_name':'','email':''};

  // Wait for the status of authentication, set scope var to true if it resolves
    djangoAuth.authenticationStatus(true).then(function(){
        $scope.authenticated = true;
        djangoAuth.profile().then(function(data){
          expires = new Date();
          expires.setDate(expires.getDate() + 1);

          $scope.user = data;
          $cookies.putObject('user',data,{'expires':expires});
        });
    });

    // Wait and respond to the logout event.
    $scope.$on('djangoAuth.logged_out', function(data) {
      $scope.authenticated = false;
      $scope.user = {'username':'','first_name':'','last_name':'','email':''};
    });
    // Wait and respond to the log in event.
    $scope.$on('djangoAuth.logged_in', function(data) {
      $scope.authenticated = true;

      djangoAuth.profile().then(function(data) {
        expires = new Date();
        expires.setDate(expires.getDate() + 1);

        $scope.user = data;
        $cookies.putObject('user',data,{'expires':expires});
      });
    });

    // If the user attempts to access a restricted page, redirect them back to the main page.
    $scope.$on('$routeChangeError', function(ev, current, previous, rejection){
      console.error("Unable to change routes.  Error: ", rejection);
      $location.path('/login').replace();
    });

    $scope.logout = function(){
      djangoAuth.logout();
    };

}]);
