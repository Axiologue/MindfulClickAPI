// Component for building list of non-Cross Referenced articles
var ArticleList = React.createClass ({displayName: "ArticleList",
  getInitialState: function() {
    return {
      data: [],
    };
  },
  render: function() {
    
    var articleNodes = this.state.data.map(function (article) {
      return (
        React.createElement(ArticleWrapper, {url: article.url, title: article.title, notes: article.notes})
      );
    });

    return ( 
      React.createElement("div", {className: "articleList row"}, 
        React.createElement("h1", null, "Add New article"), 
        React.createElement(ObjectForm, {
          id: 0, 
          submitLink: "http://localhost:8000/cross/articles/new/", 
          title: '', 
          url: '', 
          notes: ''}
        ), 
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
  handleClick: function(key) {
    this.state[key] = !this.state[key];
  },
  getInitialState: function() {
    return {
      cross: false,
      edit: false
    };
  },
  render: function() {
    var buttons = Object.keys(this.state).map(function (key) {
        var classes = "btn btn-block btn-" + key;
        return (
            React.createElement("button", {className: classes, onClick: this.handleClick.bind(this, key)}, 
              key
            )
          )
      },this);
    
    

    return (
      React.createElement("div", {className: "article listitem col-xs-12"}, 
        React.createElement("div", {className: "col-xs-12 col-sm-11"}, 
          React.createElement("ul", null, 
            React.createElement("li", null, React.createElement("strong", null, this.props.title)), 
            React.createElement("li", null, this.props.url), 
            React.createElement("li", null, this.props.notes)
          )
        ), 
        React.createElement("div", {className: "col-sm-1 col-xs-12 text-center"}, 
          buttons
        )
      )
    );
  }
});

// Form for editing and submitting articles
var ObjectForm = React.createClass ({displayName: "ObjectForm",
  handleSubmit: function(e) {
    e.preventDefault();
    console.log('submitting');
    // Programmatically get data from form
    var data = {}
    console.log(this.refs);
    Object.keys(this.props).forEach(function (element, index, array) {
      if(element != 'id' && element != 'submitLink') {
        data[element] = React.findDOMNode(this.refs[element]).value.trim();
      }
    },this);

    // Submit the new version to server
    $.ajax({
      url: this.props.submitLink,
      dataType: 'json',
      type: 'POST',
      data: data,
      success: function(data) {
        Object.keys(this.props).forEach(function (element, index, array) {
          if(element != 'id' && element != 'submitLink') {
            React.findDOMNode(this.refs[element]).value = '';
          }
        },this);

      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.submitLink, status, err.toString());
      }.bind(this)
    });

    return;
  },
  render: function() {

    // Programmatically create form elements from props that aren't the destination
    // elements or the ID
    var inputs = Object.keys(this.props).map(function (key) {
      var elID = key + this.props.id;

      if(key != 'id' && key != 'submitLink') {

        return (
          React.createElement("div", {className: "form-group"}, 
            React.createElement("label", {for: name}, key, ":"), 
            React.createElement("input", {type: "text", name: key, id: elID, className: "form-control"})
          )
        );
      }
    },this);

    return (
        React.createElement("div", {className: "col-xs-12 listitem"}, 
          React.createElement("form", {method: "post", onSubmit: this.handleSubmit}, 
            React.createElement(DjangoCSRFToken, null), 

            inputs, 

            React.createElement("input", {type: "submit", className: "btn btn-primary", value: "Submit"})

          )
        )
      );
  }
});

// Reusable CSRF token for forms
var DjangoCSRFToken = React.createClass ({displayName: "DjangoCSRFToken",

  render: function() {
    var csrftoken = $.cookie('csrftoken');

    return (
      React.createElement("input", {type: "hidden", name: "csrfmiddlewaretoken", value: csrftoken})
    );
  }
});


// Rendering live elements
React.render(
  React.createElement(ArticleList, {url: "http://localhost:8000/cross/articles"}),
  document.getElementById('Articles')
);