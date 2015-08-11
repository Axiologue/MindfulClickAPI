angular.module('cross')
.controller('ProfilePageCtrl',['$scope','$cookies',function ($scope,$cookies) {

  $scope.model = $cookies.getObject('user') || $.extend({},$scope.user);
}]);


angular.module('cross')
.controller('UserprofileCtrl', ['$scope','djangoAuth','Validate',function ($scope, djangoAuth, Validate) {
    $scope.updateProfile = function(formData, model){
      $scope.errors = [];

      Validate.form_validation(formData,$scope.errors);
      if(!formData.$invalid){
        djangoAuth.updateProfile(model)
        .then(function(data){
          // success case
          $scope.complete = true;
        },function(data){
          // error case
          $scope.error = data;
        });
      }
    };
  }]);

angular.module('cross')
.controller('LoginCtrl', ['$scope','$location','djangoAuth','Validate',function ($scope, $location, djangoAuth, Validate) {
    $scope.login = function(formData){
      $scope.errors = [];
      Validate.form_validation(formData,$scope.errors);
      if(!formData.$invalid){
        djangoAuth.login($scope.model.username, $scope.model.password)
        .then(function(data){
          // success case
          $location.path("/");
        },function(data){
          // error case
          $scope.errors = data;
        });
      }
    };
  }]);

angular.module('cross')
.controller('PasswordchangeCtrl', ['$scope','djangoAuth','Validate',function ($scope, djangoAuth, Validate) {
    $scope.model = {'new_password1':'','new_password2':''};
    $scope.complete = false;
    $scope.changePassword = function(formData){
      $scope.errors = [];
      Validate.form_validation(formData,$scope.errors);
      if(!formData.$invalid){
        djangoAuth.changePassword($scope.model.new_password1, $scope.model.new_password2)
        .then(function(data){
          // success case
          $scope.complete = true;
        },function(data){
          // error case
          $scope.errors = data;
        });
      }
    };
  }]);


angular.module('cross')
.controller('RegisterCtrl', ['$scope','djangoAuth','Validate',function ($scope, djangoAuth, Validate) {
    $scope.model = {'email':'','password':''};
    $scope.complete = false;
    $scope.register = function(formData){
      $scope.errors = [];
      Validate.form_validation(formData,$scope.errors);
      if(!formData.$invalid){
        djangoAuth.register(
            $scope.model.username,
            $scope.model.password1,
            $scope.model.password2,
            $scope.model.email
        )
        .then(function(data){
          // success case
          $scope.complete = true;
        },function(data){
          // error case
          $scope.errors = data;
        });
      }
    }
  }]);

angular.module('cross')
.controller('VerifyemailCtrl', ['$scope','$routeParams','djangoAuth',function ($scope, $routeParams, djangoAuth) {
    djangoAuth.verify($routeParams.emailVerificationToken).then(function(data){
      $scope.success = true;
    },function(data){
      $scope.failure = false;
    });
  }]);

angular.module('cross')
.controller('PasswordresetCtrl', ['$scope','djangoAuth','Validate',function ($scope, djangoAuth, Validate) {
    $scope.model = {'email':''};
    $scope.complete = false;
    $scope.resetPassword = function(formData){
      $scope.errors = [];
      Validate.form_validation(formData,$scope.errors);
      if(!formData.$invalid){
        djangoAuth.resetPassword($scope.model.email)
        .then(function(data){
          // success case
          $scope.complete = true;
        },function(data){
          // error case
          $scope.errors = data;
        });
      }
    };
  }]);

angular.module('cross')
.controller('UserprofileCtrl', ['$scope','djangoAuth','Validate',function ($scope, djangoAuth, Validate) {
    $scope.complete = false;
    $scope.updateProfile = function(formData, model){
      $scope.errors = [];
      Validate.form_validation(formData,$scope.errors);
      if(!formData.$invalid){
        djangoAuth.updateProfile(model)
        .then(function(data){
          // success case
          $scope.complete = true;
        },function(data){
          // error case
          $scope.error = data;
        });
      }
    };
  }]);

angular.module('cross')
.controller('PasswordresetconfirmCtrl', ['$scope','$routeParams','djangoAuth','Validate',function ($scope, $routeParams, djangoAuth, Validate) {
    $scope.model = {'new_password1':'','new_password2':''};
    $scope.complete = false;
    $scope.confirmReset = function(formData){
      $scope.errors = [];
      Validate.form_validation(formData,$scope.errors);
      if(!formData.$invalid){
        djangoAuth.confirmReset($routeParams.firstToken, $routeParams.passwordResetToken, $scope.model.new_password1, $scope.model.new_password2)
        .then(function(data){
          // success case
          $scope.complete = true;
        },function(data){
          // error case
          $scope.errors = data;
        });
      }
    };
  }]);
