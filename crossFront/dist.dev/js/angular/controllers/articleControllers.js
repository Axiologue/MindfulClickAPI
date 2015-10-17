angular.module('cross')
.controller('ArticleCtrl',['$scope','$http','Article','Meta',function ($scope,$http,Article,Meta) {
  $scope.csrftoken = $.cookie('csrftoken');
  $scope.articles = Article.query();
  $scope.taggedArticles = Article.queryTagged();

  Meta.query(function (data, response) {
    $scope.companies = data[0].company;
    $scope.categories = data[1].ethicssubcategory;
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

  $scope.loginModal = 'templates/includes/login_modal.html';

  // Function for button actions that can only occur when logged in
  // if Logged in, performs the action (passed in as a function)
  // if not logged in, it triggers the login modal
  $scope.ifAuthenticated = function (loggedInAction) {
    return function () {
      if($scope.authenticated) {
        loggedInAction();
      } else {
        $('#login_modal').modal('toggle');
      }
    };
  };
}]);



angular.module('cross')
.controller('SingleArticleCtrl',['$scope', 'Article',function ($scope, Article) {

  $scope.tagForm = 'templates/includes/tag_form.html';
  $scope.articleTemplate = 'templates/includes/article_base.html';
  $scope.state = {addTag:false};
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

  // if Logged in, opens the article edit form and populates it with the current article info
  $scope.readyForm = $scope.ifAuthenticated(function () {
        $scope.tempArticle = $.extend({},$scope.article);
        $scope.articleTemplate = 'templates/includes/article_form.html';
  });

  // if logged in, opens the add tag form
  $scope.toggleAddTag = $scope.ifAuthenticated(function () {
    $scope.state.addTag = !$scope.state.addTag;
  });

  // if logged in, opens the delete article modal
  $scope.articleDelete = $scope.ifAuthenticated(function () {
    $('#modal-article-' + $scope.article.id).modal('toggle');
  });

  $scope.flipBack = function () {
    $scope.articleTemplate='templates/includes/article_base.html';
  }; 

  $scope.tagCancel = function () {
    $scope.state.addTag = false;
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

  $scope.articleSubmit = $scope.ifAuthenticated(function () {
    $scope.tempArticle.csrfmiddlewaretoken = $scope.csrftoken;

    Article.save({articleID:'new'},$scope.tempArticle,function (data, response) {
      $scope.articles.push(data);
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
  });


}]);

angular.module('cross')
.controller('ArticleDeleteCtrl',['$scope','Article',function ($scope,Article) {
  $scope.modalContent = {
    id: 'modal-article-' + $scope.article.id,
    label: 'modalLabel-article-' + $scope.article.id,
    kind: 'Article',
    title: $scope.article.title,
    msg: 'This will not only remove the article, but any associated tags as well.  This cannot be undone'
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
.controller('SingleTagCtrl',['$scope','eTag',function ($scope,eTag) {
  $scope.buttons = false;
  $scope.tagUrl = 'templates/includes/tag_base.html';

  $scope.tagEdit = $scope.ifAuthenticated(function () {
    
    $scope.tagUrl = 'templates/includes/tag_form.html';

    // Get company and category ids
    $scope.newTag = $.extend({},$scope.tag);
    $scope.newTag.company = $.grep($scope.companies,function(v) {return v.name === $scope.newTag.company;})[0].id;
    var category = $.grep($scope.categories,function(v) {return v.name === $scope.newTag.tag_type.subcategory;})[0];
    $scope.newTag.subcategory = category.id;

    // Add the appropriate tagTypes for that category
    $scope.tagTypes = category.tag_types;
    $scope.newTag.tag_type = $scope.tag.tag_type.id;
  });

  $scope.tagDelete = $scope.ifAuthenticated(function () {
    $('#modal-tag-' + $scope.article.id + '-' + $scope.tag.id).modal('toggle');
  });

  $scope.tagCancel = function () {
    
    $scope.tagUrl = 'templates/includes/tag_base.html';

  };

  $scope.tagSubmit = function () {
    $scope.newTag.article = $scope.article.id;

    eTag.update({tagID:$scope.tag.id},$scope.newTag,function (data, response) {

      // Replace element IDs with actual names
      data.company = $.grep($scope.companies,function(v) {return v.id === data.company;})[0].name;
      var category = $.grep($scope.categories,function(v) {return v.id === $scope.newTag.subcategory;})[0];

      data.tag_type = {
        name: $.grep(category.tag_types, function(v) {return v.id === data.tag_type;})[0].name,
        subcategory: category.name,
        id: data.tag_type
      };

      $scope.tag = $.extend({},data);
      $scope.error.error = false;

      $scope.tagUrl = 'templates/includes/tag_base.html';

    }, function (response) {
      $scope.error.msg = JSON.stringify(response.data);
      $scope.error.error = true;
    });
  };

}]);

angular.module('cross')
.controller('NewTagCtrl',['$scope','eTag',function ($scope,eTag) {
  $scope.newTag = {
    company: "",
    subcategory: "",
    tag_type: "",
    excerpt: "",
    value: undefined,
    article: $scope.article.id
  };

  $scope.tagSubmit = function () {
    $scope.newTag.csrfmiddlewaretoken = $scope.csrftoken;

    eTag.save({tagID: 'new'},$scope.newTag,function (data,response) {
      $scope.article.ethicstags = $scope.article.ethicstags || [];

      // Replace element IDs with actual names
      data.company = $.grep($scope.companies,function(v) {return v.id === data.company;})[0].name;
      var category = $.grep($scope.categories,function(v) {return v.id === $scope.newTag.subcategory;})[0];

      data.tag_type = {
        name: $.grep(category.tag_types, function(v) {return v.id === data.tag_type;})[0].name,
        subcategory: category.name,
        id: data.tag_type
      };

      $scope.article.ethicstags.push(data);
      $scope.state.addTag = false;
      $scope.error.error = false;

      //if the article is in the Unanalyzed list, move it to the analyzed list
      if($scope.article.ethicstags.length === 1) {
        $scope.taggedArticles.push($scope.article);
        $scope.removeFromList($scope.article,$scope.articles);
      }

      // Reset the newTag to blank, in case you want to add more tags
      $scope.newTag = {
        company: "",
        subcategory: "",
        tag_type: "",
        excerpt: "",
        value: undefined,
        article: $scope.article.id
      };
    },function (response) {
      $scope.error.msg = JSON.stringify(response.data);
      $scope.error.error = true;
    });   
  };

  

}]);

angular.module('cross')
.controller('TagFormCtrl',['$scope','eType',function ($scope,eType) {
  $scope.tagFormState = {
    addTagType: false
  };

  $scope.newTagType = {
    name: ''
  };

  // Shows the form to add new Tag Type
  $scope.showNewTagType = function ($event) {
    $event.preventDefault();
    $event.stopPropagation();

    $scope.tagFormState.addTagType = !$scope.tagFormState.addTagType;
  };

  // Submit a New Tag Type
  $scope.submitTagType = function ($event) {
    $event.preventDefault();
    $event.stopPropagation();

    // Get the currently selected subcategory
    $scope.newTagType.subcategory = $scope.newTag.subcategory;

    // Send the new TagType to server
    eType.save($scope.newTagType,function (data, respone) {

      // Get index of current subcategory
      var index = 0;
      $scope.categories.some(function(elem, i) {
        if (elem.id === $scope.newTag.subcategory) {
          index = i;
          return true;
        }
      });

      // Add the new Tag Type to the current category list
      $scope.categories[index].tag_types.push(data);

      // Set the form to the new TagTpe
      $scope.newTag.tag_type = data.id;

      // Reset the add Tag Type form to invisible
      $scope.tagFormState.addTagType = false;
    },function (response) {
      console.log(response.data);
      $scope.error.msg = JSON.stringify(response.data);
      $scope.error.error = true;
    });
  };

  // Switches to the appropriate set of TagTypes when an ethical category is selected
  $scope.loadFacts = function () {
    $scope.tagTypes = $.grep($scope.categories,function(v) {return v.id === $scope.newTag.subcategory;})[0].tag_types;
  };

}]);

angular.module('cross')
.controller('DeleteTagCtrl',['$scope','eTag',function ($scope,eTag) {
  $scope.modalContent = {
    id: 'modal-tag-' + $scope.article.id + '-' + $scope.tag.id,
    label: 'modalLabel-cross-' + $scope.article.id + '-' + $scope.tag.id,
    kind: 'Tag',
    title: $scope.tag.tag_type.name + " on " + $scope.article.title,
    msg: 'This cannot be undone'
  };

  $scope.itemDelete = function () {

    eTag.delete({tagID:$scope.tag.id}, function (data,response) {
      $scope.removeFromList($scope.tag,$scope.article.ethicstags);
      if ($scope.article.ethicstags.length === 0) {
        $scope.removeFromList($scope.article,$scope.taggedArticles);
        $scope.articles.push($scope.article);
      }

      $('myModal' + $scope.article.id).modal('toggle');
      $('body').removeClass('modal-open');
      $('.modal-backdrop').remove();
    });
  };
}]);

angular.module('cross')
.controller('LoginModalCtrl',['$scope','$location',function ($scope,$location) {
  $scope.goToLogin = function () {
    $location.path('/login'); 
    $('body').removeClass('modal-open');
    $('.modal-backdrop').remove();
  };

  $scope.goToSignUp = function() {
    $location.path('/signUp');
    $('body').removeClass('modal-open');
    $('.modal-backdrop').remove();
  };
}]);
