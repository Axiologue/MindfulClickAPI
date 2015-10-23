angular.module('cross')
.controller('EthicsProfileCtrl',['$scope','Pref',function($scope,Pref) {
  $scope.prefs = Pref.query(); 

  $scope.longerThanZero = function (prop) {
    return function (item) {
      return item[prop].length > 0;
    }
  };
}]);

// Controller for editing profile preferences
angular.module('cross')
.controller('PrefEditCtrl',['$scope','Pref',function ($scope, Pref) {

  $scope.profileState = {
    editPref: false
  };

  
  $scope.editPref = function () {
    $scope.profileState.editPref = true;

    // Store old version of the preference for cancellation
    $scope.oldPref = $scope.pref.preference;
  };

  $scope.savePref = function () {
    Pref.update({prefID:$scope.pref.id},$scope.pref, function () {
      $scope.profileState.editPref = false;
    },function (response) {
      var error = JSON.stringify(response.data);
      console.log(error);
    });
  };

  $scope.cancelEdit = function () {
    $scope.pref.preference = $scope.oldPref;

    // Load old version of the preference for cancel
    $scope.profileState.editPref = false;
  };
}]);
