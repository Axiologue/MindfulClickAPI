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
        React.createElement(ArticleWrapper, {
          url: article.url, 
          title: article.title, 
          notes: article.notes, 
          id: article.id, 
          key: article.id, 
          deleteItem: this.deleteItem})
      );
    },this);

    return ( 
      React.createElement("div", {className: "articleList row"}, 
        React.createElement("h1", null, "Add New article"), 
        React.createElement(ArticleForm, {
          id: 0, 
          submitLink: "http://localhost:8000/cross/articles/new/", 
          title: '', 
          url: '', 
          notes: '', 
          header: "POST"}), 
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
  },
  deleteItem: function (id) {
    $.ajax({
      url: "http://localhost:8000/cross/articles/delete/" + id + "/",
      dataType: 'json',
      type: 'DELETE',
      cache: false,
      success: function(data) {
        // 
        var index;
        state.data.some(function(entry, i) {
            if (entry.id == id) {
                index = i;
                return true;
            }
        });
        state.data.splice(index,1);

        setState({data: state.data});
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
      title: this.props.title,
      url: this.props.url,
      notes: this.props.notes,
    };
  },
  onFormSuccess: function(data) {
    this.setState({edit: false,
                   title: data['title'],
                   url: data['url'],
                   notes: data['notes']
                 });
  },
  render: function() {
    var buttons = ['cross','edit'].map(function (key) {
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
                React.createElement("li", null, React.createElement("h3", null, this.state.title)), 
                React.createElement("li", null, React.createElement("a", {href: this.state.url}, this.state.url)), 
                React.createElement("li", null, this.state.notes)
              )
            ), 
            React.createElement("div", {className: "col-sm-2 col-xs-12 text-center"}, 
              buttons, 
              React.createElement("button", {className: "btn btn-block btn-delete", 
                  "data-toggle": "modal", 
                  "data-target": '#myModal' + this.props.id, 
                  type: "button"}, "delete")
            ), 

            React.createElement(WarningModal, {message: 'Are you sure you want to delete the article "' + this.state.title + '"?', 
              id: this.props.id, 
              title: "Delete article?", 
              buttonText: "Delete", 
              action: this.props.deleteItem})
          )
        );
    }
    
    if (this.state.edit) {
      var normalView = React.createElement(ArticleForm, {
        title: this.state.title, 
        url: this.state.url, 
        notes: this.state.notes, 
        submitLink: 'http://localhost:8000/cross/articles/update/' + this.props.id + '/', 
        id: this.props.id, 
        header: "PUT", 
        formSuccess: this.onFormSuccess})

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
      data[element] = React.findDOMNode(this.refs[element]).getElementsByClassName('form-control')[0].value.trim();
    },this);

    // Passing an id of 0 means it's a new object, so we don't want to send an ID
    if(data['id'] === 0) {
      delete data['id'];
    }

    // Submit the new version to server
    $.ajax({
      url: this.props.submitLink,
      dataType: 'json',
      type: this.props.header,
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

        this.props.formSuccess(data);

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

            React.createElement(FormHiddenElement, {name: "id", value: this.props.id, ref: "id"}), 

            React.createElement(FormInputElement, {element: "title", type: "text", id: this.props.id, value: this.props.title, ref: "title"}), 

            React.createElement(FormInputElement, {element: "url", type: "text", id: this.props.id, value: this.props.url, ref: "url"}), 

            React.createElement(FormTextAreaElement, {element: "notes", id: this.props.id, value: this.props.notes, ref: "notes"}), 

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

var FormInputElement = React.createClass ({displayName: "FormInputElement",
  getInitialState: function() {
    return {
      initial: this.props.value
    }
  },
  render: function() {
    var elID = this.props.element + this.props.id;

    return (
      React.createElement("div", {className: "form-group"}, 
        React.createElement("label", {for: elID}, this.props.element.toUpperCase(), ":"), 
        React.createElement("input", {type: this.props.type, 
          name: this.props.element, 
          id: elID, className: "form-control", 
          value: this.state.initial, 
          onChange: this.onChange})
      )
    );
  },
  onChange: function(e) {
    this.setState({ initial: e.target.value });
  }
});

var FormTextAreaElement = React.createClass ({displayName: "FormTextAreaElement",
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

var FormHiddenElement = React.createClass ({displayName: "FormHiddenElement",
  render: function() {
    return (
      React.createElement("div", null, 
        React.createElement("input", {type: "hidden", className: "form-control", name: this.props.name, value: this.props.value})
      )
      )
  }
})

var WarningModal = React.createClass ({displayName: "WarningModal",
  handleClick: function() {
    this.props.action(this.props.id);
    $('myModal' + this.props.id).modal('hide');
  },
  render: function() {
    return (
      React.createElement("div", {id: "myModal" + this.props.id, className: "modal fade", tabindex: "-1", role: "dialog", "aria-labelledby": "myModalLabel" + this.props.id}, 
        React.createElement("div", {className: "modal-dialog", role: "document"}, 
          React.createElement("div", {className: "modal-content"}, 
            React.createElement("div", {className: "modal-header"}, 
              React.createElement("button", {type: "button", className: "close", "data-dismiss": "modal", "aria-label": "Close"}, React.createElement("span", {"aria-hidden": "true"}, "×")), 
              React.createElement("h4", {className: "modal-title", id: "myModalLabel" + this.props.id}, this.props.title)
            ), 
            React.createElement("div", {className: "modal-body"}, 
              React.createElement("p", null, this.props.message)
            ), 
            React.createElement("div", {className: "modal-footer"}, 
              React.createElement("button", {type: "button", className: "btn btn-default", "data-dismiss": "modal"}, "Close"), 
              React.createElement("button", {type: "button", className: "btn btn-primary", onClick: this.handleClick}, this.props.buttonText)
            )
          )
        )
      )
    );
  }
})


// Rendering live elements
React.render(
  React.createElement(ArticleList, {url: "http://localhost:8000/cross/articles"}),
  document.getElementById('articles')
);

React.render(
  React.createElement(CrossList, {url: "http://localhost:8000/cross/cross-list"}),
  document.getElementById('cross')
);