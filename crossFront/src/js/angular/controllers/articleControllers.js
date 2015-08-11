angular.module('cross')
.controller('ArticleCtrl',['$scope','$http','Article','Cross','Meta',function ($scope,$http,Article,Cross,Meta) {
  $scope.csrftoken = $.cookie('csrftoken');
  $scope.articles = Article.query();
  $scope.crossList = Cross.query();

  Meta.query(function (value, response) {
    $scope.companies = value[0].company;
    $scope.categories = value[1].ethicssubcategory;
  });

  $scope.deleteModal = 'templates/includes/delete_modal.html';

  $scope.removeFromList = function (item, list) {
    var index = 0;
      list.some(function(elem, i) {
        if (elem.id === item.id) {
          index = i;
          return true;
        }
      });
      list.splice(index,1);
  };
}]);



angular.module('cross')
.controller('SingleArticleCtrl',['$scope', 'Article','Cross',function ($scope, Article, Cross) {

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
  };

  $scope.flipBack = function () {
    $scope.articleTemplate='templates/includes/article_base.html';
  }; 

}]);

angular.module('cross')
.controller('NewArticleCtrl',['$scope','Article',function ($scope, Article) {
  $scope.articleForm = 'templates/includes/article_form.html';
  $scope.error = {error: false,
                  msg: ""};
  $scope.success = {success: false,
                    msg: "Your article has been sucessfully submitted"};

  $scope.tempArticle = {
    id: 0,
    url: "",
    title: "",
    notes: ""
  };

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

angular.module('cross')
.controller('ArticleDeleteCtrl',['$scope','Article',function ($scope,Article) {
  $scope.modalContent = {
    id: 'modal-article-' + $scope.article.id,
    label: 'modalLabel-article-' + $scope.article.id,
    kind: 'Article',
    title: $scope.article.title,
    msg: 'This will not only remove the article, but any associated analysis that has been done on it.  This cannot be undone'
  };

  $scope.itemDelete = function () {
    $scope.article.csrfmiddlewaretoken = $scope.csrftoken;

    Article.delete({articleID: $scope.article.id},function () {
      if ($scope.articles.some(function (element, index, array) { return element.id === $scope.article.id; })) {
        $scope.removeFromList($scope.article,$scope.articles);
      } else {
        $scope.removeFromList($scope.article,$scope.crossList);
      }
      

      $('myModal' + $scope.article.id).modal('toggle');
      $('body').removeClass('modal-open');
      $('.modal-backdrop').remove();
    });
  };
}]);

angular.module('cross')
.controller('SingleCrossCtrl',['$scope','Cross',function ($scope,Cross) {
  $scope.buttons = false;
  $scope.crossUrl = 'templates/includes/cross_base.html';

  $scope.crossEdit = function () {
    
    $scope.crossUrl = 'templates/includes/cross_form.html';
    $scope.newCross = $.extend({},$scope.cross);
    $scope.newCross.company = $.grep($scope.companies,function(v) {return v.name === $scope.newCross.company;})[0].id;
    $scope.newCross.subcategory = $.grep($scope.categories,function(v) {return v.name === $scope.newCross.subcategory;})[0].id;
  };

  $scope.crossCancel = function () {
    
    $scope.crossUrl = 'templates/includes/cross_base.html';

  };

  $scope.crossSubmit = function () {
    $scope.newCross.article = $scope.article.id;

    Cross.update({crossID:$scope.cross.id},$scope.newCross,function (value, response) {
      // Replace element IDs with actual names
      value.company = $.grep($scope.companies,function(v) {return v.id === value.company;})[0].name;
      value.subcategory = $.grep($scope.categories,function(v) {return v.id === value.subcategory;})[0].name;

      $scope.cross = $.extend({},value);
      $scope.error.error = false;

      $scope.crossUrl = 'templates/includes/cross_base.html';

    }, function (response) {
      $scope.error.msg = JSON.stringify(response.data);
      $scope.error.error = true;
    });
  };
}]);

angular.module('cross')
.controller('NewCrossCtrl',['$scope','Cross',function ($scope,Cross) {
  $scope.newCross = {
    company: "",
    subcategory: "",
    notes: "",
    score: "",
    article: $scope.article.id
  };

  $scope.crossSubmit = function () {
    $scope.newCross.csrfmiddlewaretoken = $scope.csrftoken;


    Cross.save({crossID: 'new'},$scope.newCross,function (value,response) {
      $scope.article.data = $scope.article.data || [];

      // Replace element IDs with actual names
      value.company = $.grep($scope.companies,function(v) {return v.id === value.company;})[0].name;
      value.subcategory = $.grep($scope.categories,function(v) {return v.id === value.subcategory;})[0].name;

      $scope.article.data.push(value);
      $scope.analysis.analysis = false;
      $scope.error.error = false;

      //if the article is in the Unanalyzed list, move it to the analyzed list
      if($scope.article.data.length === 1) {
        $scope.crossList.push($scope.article);
        $scope.removeFromList($scope.article,$scope.articles);
      }
    },function (response) {
      $scope.error.msg = JSON.stringify(response.data);
      $scope.error.error = true;
    });   
  };

}]);

angular.module('cross')
.controller('CrossDeleteCtrl',['$scope','Cross',function ($scope,Cross) {
  $scope.modalContent = {
    id: 'modal-cross-' + $scope.article.id + '-' + $scope.cross.id,
    label: 'modalLabel-cross-' + $scope.article.id + '-' + $scope.cross.id,
    kind: 'Analysis',
    title: $scope.cross.subcategory + ': ' + $scope.cross.score,
    msg: 'This cannot be undone'
  };

  $scope.itemDelete = function () {

    Cross.delete({crossID:$scope.cross.id}, function (value,response) {
      $scope.removeFromList($scope.cross,$scope.article.data);
      if ($scope.article.data.length === 0) {
        $scope.removeFromList($scope.article,$scope.crossList);
        $scope.articles.push($scope.article);
      }

      $('myModal' + $scope.article.id).modal('toggle');
      $('body').removeClass('modal-open');
      $('.modal-backdrop').remove();
    });
  };
}]);