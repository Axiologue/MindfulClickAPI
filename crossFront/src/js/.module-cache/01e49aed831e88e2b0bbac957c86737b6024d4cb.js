// ARTICLE COMPONENTS

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
        React.createElement(ArticleWrapper, {url: article.url, title: article.title, notes: article.notes, id: article.id, key: article.id})
      );
    });

    return ( 
      React.createElement("div", {className: "articleList row"}, 
        React.createElement("h1", null, "Add New article"), 
        React.createElement(ArticleForm, {
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

    this.setState(this.state);
  },
  getInitialState: function() {
    return {
      cross: false,
      edit: false,
      delete: false,
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
    
    
    if (!this.state.cross && !this.state.edit) {
      var normalView = (
          React.createElement("div", {className: "article listitem col-xs-12"}, 
            React.createElement("div", {className: "col-xs-12 col-sm-10"}, 
              React.createElement("ul", null, 
                React.createElement("li", null, React.createElement("h3", null, this.props.title)), 
                React.createElement("li", null, React.createElement("a", {href: this.props.url}, this.props.url)), 
                React.createElement("li", null, this.props.notes)
              )
            ), 
            React.createElement("div", {className: "col-sm-2 col-xs-12 text-center"}, 
              buttons
            )
          )
        );
    }
    
    if (this.state.edit) {
      var normalView = React.createElement(ArticleForm, {
        title: this.props.title, 
        url: this.props.url, 
        notes: this.props.notes, 
        submitLink: 'http://localhost:8000/articles/update/' + this.props.id, 
        id: this.props.id})

    }

    return (
      React.createElement("div", null, 
        normalView
      )
    );
  }
});

// Form for editing and submitting articles
var ArticleForm = React.createClass ({displayName: "ArticleForm",
  handleSubmit: function(e) {
    e.preventDefault();
    // Programmatically get data from form
    var data = {}
    Object.keys(this.refs).forEach(function (element, index, array) {
      data[element] = React.findDOMNode(this.refs[element]).value.trim();
    },this);

    // Passing an id of 0 means it's a new object, so we don't want to send an ID
    if(data['id'] === 0) {
      delete data['id'];
    }

    // Submit the new version to server
    $.ajax({
      url: this.props.submitLink,
      dataType: 'json',
      type: 'POST',
      data: data,
      success: function(data) {
        
        // Add success message
        this.setState({
          error: '',
          success: 'Your article has been successfully added!'
        });

        // Reset Form to blank if new article
        if(!data['id']) {       
          React.findDOMNode(this.refs['title']).value = '';
          React.findDOMNode(this.refs['url']).value = '';
          React.findDOMNode(this.refs['notes']).value = '';
        }

      }.bind(this),
      error: function(xhr, status, err) {
        this.setState({
          error: xhr.responseText.toString(),
          success: ''
        });

      }.bind(this)
    });

    return;
  },
  getInitialState: function () {
    return {
      success: '',
      error: ''
    };
  },
  render: function() {


    return (
        React.createElement("div", {className: "col-xs-12 listitem"}, 

          React.createElement("h3", {className: "text-danger"}, this.state.error), 
          React.createElement("h3", {className: "text-success"}, this.state.success), 

          React.createElement("form", {method: "post", onSubmit: this.handleSubmit}, 
            React.createElement(DjangoCSRFToken, null), 

            React.createElement("input", {type: "hidden", name: "id", value: this.props.id, ref: "id"}), 

            React.createElement(TextFormElement, {element: "title", id: this.props.id, value: this.props.title}), 

            React.createElement(TextFormElement, {element: "url", id: this.props.id, value: this.props.url}), 

            React.createElement(TextAreaFormElement, {element: "notes", id: this.props.id, value: this.props.notes}), 

            React.createElement("input", {type: "submit", className: "btn btn-primary", value: "Submit"})

          )
        )
      );
  }
});

// CROSS REFERENCE COMPONENTS

// Component for building list of non-Cross Referenced articles
var CrossList = React.createClass ({displayName: "CrossList",
  getInitialState: function() {
    return {
      data: [],
    };
  },
  render: function() {
    
    var crossNodes = this.state.data.map(function (cross) {
      return (
        React.createElement(CrossWrapper, {url: cross.url, title: cross.title, data: cross.data})
      );
    });

    return ( 
      React.createElement("div", {className: "crossList row"}, 
        React.createElement("h1", null, "Cross-Referenced Articles"), 
        crossNodes
      )
    );
  },
  componentDidMount: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      success: function(data) {
        console.log(data);
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  }
});

var CrossWrapper = React.createClass ({displayName: "CrossWrapper",
  render: function() {
    var crossData = this.props.data.map(function (cross) {
      return (
        React.createElement("li", null, React.createElement("strong", null, cross.company, " ", cross.product), React.createElement("br", null), 
          React.createElement("ul", null, 
            React.createElement("li", null, React.createElement("strong", null, cross.subcategory), ": ", cross.score), 
            React.createElement("li", null, cross.notes)
          )
        )
      );
    });

    return (
      React.createElement("div", {className: "cross listitem col-xs-12"}, 
        React.createElement("div", {className: "col-xs-12 col-sm-11"}, 
          React.createElement("ul", null, 
            React.createElement("li", null, React.createElement("h3", null, this.props.title)), 
            React.createElement("li", null, React.createElement("a", {href: this.props.url}, this.props.url)), 
            React.createElement("li", null, this.props.notes), 
            crossData
          )
        )
      )
    );
  }
});

// REUSABLE COMPONENTS

// Reusable CSRF token for forms
var DjangoCSRFToken = React.createClass ({displayName: "DjangoCSRFToken",

  render: function() {
    var csrftoken = $.cookie('csrftoken');

    return (
      React.createElement("input", {type: "hidden", name: "csrfmiddlewaretoken", value: csrftoken})
    );
  }
});

var TextFormElement = React.createClass ({displayName: "TextFormElement",
  render: function() {
    var elID = this.props.element + this.props.id;
    var initial = this.props.value;

    return (
      React.createElement("div", {className: "form-group"}, 
        React.createElement("label", {for: elID}, this.props.element.toUpperCase(), ":"), 
        React.createElement("input", {type: "text", 
          name: this.props.element, 
          id: elID, className: "form-control", 
          ref: this.props.element, 
          value: initial})
      )
    );
  }
});

var TextAreaFormElement = React.createClass ({displayName: "TextAreaFormElement",
  render: function() {
    var elID = this.props.element + this.props.id;

    return (
      React.createElement("div", {className: "form-group"}, 
        React.createElement("label", {for: elID}, this.props.element.toUpperCase(), ":"), 
        React.createElement("textarea", {
          rows: 3, 
          name: this.props.element, 
          id: elID, 
          className: "form-control", 
          ref: this.props.element}, this.props.value)
      )
    );
  }
});


// Rendering live elements
React.render(
  React.createElement(ArticleList, {url: "http://localhost:8000/cross/articles"}),
  document.getElementById('articles')
);

React.render(
  React.createElement(CrossList, {url: "http://localhost:8000/cross/cross-list"}),
  document.getElementById('cross')
);