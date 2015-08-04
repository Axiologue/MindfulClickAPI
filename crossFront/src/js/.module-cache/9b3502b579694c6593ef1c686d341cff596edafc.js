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
  },
  componentDidMount: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  }
});

// Wrapper class for the individual non-Cross Referenced articles
var ArticleWrapper = React.createClass ({displayName: "ArticleWrapper",
  render: function() {
    return (
      React.createElement("div", {className: "article listitem col-xs-12"}, 
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
  React.createElement(ArticleList, {url: "http://localhost:8000/cross/articles/"}),
  document.getElementById('Articles')
);