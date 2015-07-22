'use strict';

var crossControllers = angular.module('crossControllers',[]);

crossControllers.controller('BodyCtrl',['$scope',function ($scope, Articles) {
  $scope.csrftoken = $.cookie('csrftoken');
}]);

crossControllers.controller('ArticleListCtrl',['$scope','Article',function ($scope, Article) {
  $scope.articles = Article.query();

}]);

crossControllers.controller('SingleArticleCtrl',['$scope', 'Article',function ($scope, Article) {
  $scope.edit = false;
  $scope.add_analysis = false;
  $scope.error = {
    error: false,
    msg: ""
  };


  $scope.articleSubmit = function () {
    $scope.tempArticle.csrfmiddlewaretoken = $scope.csrftoken;

    Article.update({articleID: $scope.article.id},$scope.tempArticle,function () {
      $scope.edit = false;
      $scope.article = $.extend({},$scope.tempArticle);
    },function (response) {
      $scope.error.msg = JSON.stringify(response.data);
      $scope.error.error = true;
    });
  };

  $scope.readyForm = function() {
    $scope.tempArticle = $.extend({},$scope.article);
    $scope.edit = !$scope.edit;
  }

  $scope.articleDelete = function () {
    Article.delete({articleID: $scope.article.id},function () {
      var index = 0;
      $scope.articles.some(function(article, i) {
        if (article.id === $scope.article.id) {
          index = i;
          return true;
        }
      });
      $scope.articles.splice(index,1);

      $('myModal' + $scope.article.id).modal('toggle');
      $('body').removeClass('modal-open');
      $('.modal-backdrop').remove();
    });
  }

}]);

crossControllers.controller('NewArticleCtrl',['$scope','Article',function ($scope, Article) {
  $scope.error = {error: false,
                  msg: ""};
  $scope.success = {success: false,
                    msg: "Your article has been sucessfully submitted"}

  $scope.article = {
    id: 0,
    url: "",
    title: "",
    notes: ""
  }

  $scope.articleSubmit = function () {
    $scope.article.csrfmiddlewaretoken = $scope.csrftoken;

    Article.save({articleID:'new'},$scope.article,function (value, response) {
      $scope.articles.push(value);
      $scope.article = {
        id: 0,
        url: "",
        title: "",
        notes: ""
      };
      $scope.error.error = false;
      $scope.success.success = true;
    },function (response) {
      $scope.error.msg = JSON.stringify(response.data);
      $scope.error.error = true;
      $scope.success.success = false;
    });
  };
}]);