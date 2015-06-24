// Component for building list of non-Cross Referenced articles
var ArticleList = React.createClass ({displayName: "ArticleList",
  getInitialState: function() {
    return {data: []};
  },
  render: function() {
    
    var articleNodes = this.state.data.map(function (article) {
      return (
        React.createElement(ArticleWrapper, {url: article.url, title: article.title, notes: article.notes})
      );
    });

    return ( 
      React.createElement("div", {className: "articleList row"}, 
        React.createElement("h1", null, "Unreferenced Articles"), 
        articleNodes
      )
    );
  }
});

// Wrapper class for the individual non-Cross Referenced articles
var ArticleWrapper = React.createClass ({displayName: "ArticleWrapper",
  render: function() {
    return (
      React.createElement("div", {className: "article col-xs-12"}, 
        React.createElement("ul", null, 
          React.createElement("li", null, React.createElement("strong", null, this.props.title)), 
          React.createElement("li", null, this.props.url), 
          React.createElement("li", null, this.props.notes)
        )
      )
    );
  }
});


// Rendering live elements
React.render(
  React.createElement(ArticleList,null),
  document.getElementById('Articles')
);