'use strict';

var crossControllers = angular.module('crossControllers',[]);

crossControllers.controller('BodyCtrl',['$scope','$http','Article','Cross',function ($scope,$http,Article,Cross) {
  $scope.csrftoken = $.cookie('csrftoken');
  $scope.articles = Article.query();
  $scope.crossList = Cross.query();

  $http.get('http://localhost:8000/cross/formMeta/').success(function (data) {
    $scope.companies = data[0].company;
    $scope.categories = data[1].ethicssubcategory;
  });
}]);



crossControllers.controller('SingleArticleCtrl',['$scope', 'Article','Cross',function ($scope, Article, Cross) {
  function removeArticle (elements) {
    var index = 0;
      elements.some(function(article, i) {
        if (article.id === $scope.article.id) {
          index = i;
          return true;
        }
      });
      elements.splice(index,1);
  }

  $scope.crossForm = 'templates/includes/cross_form.html';
  $scope.articleTemplate = 'templates/includes/article_base.html';
  $scope.analysis = {analysis:false};
  $scope.error = {
    error: false,
    msg: ""
  };
  $scope.cancel = true;

  $scope.articleSubmit = function () {
    $scope.tempArticle.csrfmiddlewaretoken = $scope.csrftoken;

    Article.update({articleID: $scope.article.id},$scope.tempArticle,function () {
      $scope.articleTemplate = 'templates/includes/article_base.html';
      $scope.article = $.extend({},$scope.tempArticle);
    },function (response) {
      $scope.error.msg = JSON.stringify(response.data);
      $scope.error.error = true;
    });
  };

  $scope.readyForm = function() {
    $scope.tempArticle = $.extend({},$scope.article);
    $scope.articleTemplate = 'templates/includes/article_form.html';
  }

  $scope.flipBack = function () {
    $scope.articleTemplate='templates/includes/article_base.html';
  }

  $scope.articleDelete = function () {
    $scope.article.csrfmiddlewaretoken = $scope.csrftoken;

    Article.delete({articleID: $scope.article.id},function () {
      if ($scope.articles.some(function (element, index, array) { return element.id === $scope.article.id; })) {
        removeArticle($scope.articles);
      } else {
        removeArticle($scope.crossList);
      }
      

      $('myModal' + $scope.article.id).modal('toggle');
      $('body').removeClass('modal-open');
      $('.modal-backdrop').remove();
    });
  }

  

  

}]);

crossControllers.controller('NewArticleCtrl',['$scope','Article',function ($scope, Article) {
  $scope.articleForm = 'templates/includes/article_form.html'
  $scope.error = {error: false,
                  msg: ""};
  $scope.success = {success: false,
                    msg: "Your article has been sucessfully submitted"}

  $scope.tempArticle = {
    id: 0,
    url: "",
    title: "",
    notes: ""
  }

  $scope.articleSubmit = function () {
    $scope.tempArticle.csrfmiddlewaretoken = $scope.csrftoken;

    Article.save({articleID:'new'},$scope.tempArticle,function (value, response) {
      $scope.articles.push(value);
      $scope.tempArticle = {
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

crossControllers.controller('SingleCrossCtrl',['$scope',function ($scope) {
  $scope.buttons = false;
}]);

crossControllers.controller('NewCrossCtrl',['$scope','Cross',function ($scope,Cross) {
  $scope.newCross = {
    company: "",
    subcategory: "",
    notes: "",
    score: "",
    article: $scope.article.id
  }

  function removeArticle (elements) {
    var index = 0;
    elements.some(function(article, i) {
      if (article.id === $scope.article.id) {
        index = i;
        return true;
      }
    });
    elements.splice(index,1);
  }

  $scope.CrossSubmit = function () {
    $scope.newCross.csrfmiddlewaretoken = $scope.csrftoken;


    Cross.save({crossID: 'new'},$scope.newCross,function (value,response) {
      $scope.article.data = $scope.article.data || [];

      // Replace element IDs with actual names
      value.company = $.grep($scope.companies,function(v) {return v.id === value.company})[0].name;
      value.subcategory = $.grep($scope.categories,function(v) {return v.id === value.subcategory})[0].name;

      $scope.article.data.push(value);
      $scope.analysis.analysis = false;
      $scope.error.error = false;

      //if the article is in the Unanalyzed list, move it to the analyzed list
      if($scope.article.data.length === 1) {
        $scope.crossList.push($scope.article);
        removeArticle($scope.articles);
      }
    },function (response) {
      $scope.error.msg = JSON.stringify(response.data);
      $scope.error.error = true;
    });   
  }
}]);