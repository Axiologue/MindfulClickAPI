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
            React.createElement("li", null, React.createElement("h3", null, this.props.title)), 
            React.createElement("li", null, React.createElement("a", {href: this.props.url}, this.props.url)), 
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
        // remove an exiting errors
        this.state.error = null;

        // Add success message
        this.state.success = 'Your article has been successfully added!'

        // Reset Form to blank if new article
        if(!data['id']) {       
          React.findDOMNode(this.refs['title']).value = '';
          React.findDOMNode(this.refs['url']).value = '';
          React.findDOMNode(this.refs['notes']).value = '';
        }

      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.submitLink, status, err.toString());

        this.state.error = err.toString();

        this.state.success = null;

      }.bind(this)
    });

    return;
  },
  getInitialState: function () {
    return {
      success: null,
      error: null
    };
  },
  render: function() {

    var titleID = 'title' + this.props.id;
    var urlID = 'url' + this.props.id;
    var notesID = 'notes' + this.props.id;

    // Create errors message for any errors
    var Msg = function() {
      if(this.state.error) {
        return (
            React.createElement("h3", {className: "text-danger"}, this.state.error)
          );
      }
      if(this.state.success) {
        return (
            React.createElement("h3", {className: "text-success"}, this.state.success)
          );
      }
    }

    return (
        React.createElement("div", {className: "col-xs-12 listitem"}, 
          {Msg}, 
          React.createElement("form", {method: "post", onSubmit: this.handleSubmit}, 
            React.createElement(DjangoCSRFToken, null), 

            React.createElement("div", {className: "form-group"}, 
              React.createElement("label", {for: titleID}, "Title:"), 
              React.createElement("input", {type: "text", name: "title", id: titleID, className: "form-control", ref: "title"})
            ), 

            React.createElement("div", {className: "form-group"}, 
              React.createElement("label", {for: urlID}, "URL:"), 
              React.createElement("input", {type: "text", name: "url", id: urlID, className: "form-control", ref: "url"})
            ), 

            React.createElement("div", {className: "form-group"}, 
              React.createElement("label", {for: notesID}, "Notes:"), 
              React.createElement("textarea", {name: "notes", id: notesID, className: "form-control", ref: "notes", rows: 3})
            ), 

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