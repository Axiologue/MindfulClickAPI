// ARTICLE COMPONENTS

// Component for building list of non-Cross Referenced articles
var ArticleList = React.createClass ({displayName: "ArticleList",
  getInitialState: function() {
    return {
      data: [ {article: []},
              {ethicscategory: []},
              {company: []} ]
    };
  },
  render: function() {
    
    var articleNodes = this.state.data[0].article.map(function (article) {
      return (
        React.createElement(ArticleWrapper, {
          url: article.url, 
          title: article.title, 
          notes: article.notes, 
          id: article.id, 
          key: article.id, 
          deleteItem: this.deleteItem, 
          companies: this.state.data[2]['company'], 
          categories: this.state.data[1]['ethicscategory']})
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
        React.createElement("h1", null, "Unanalyzed Articles"), 
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
        this.state.data.some(function(entry, i) {
            if (entry.id == id) {
                index = i;
                return true;
            }
        });
        this.state.data.splice(index,1);

        this.setState({data: this.state.data});
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
      add_analysis: false,
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
    var buttons = ['add_analysis','edit'].map(function (key) {
        var classes = "btn btn-block btn-" + key;
        return (
            React.createElement("button", {className: classes, onClick: this.handleClick.bind(this, key)}, 
              key.replace("_"," ")
            )
          )
      },this);

    if(this.state.add_analysis) {
      var crossForm = (
          React.createElement(CrossForm, {
             article_id: this.props.id, 
             companies: this.props.companies, 
             categories: this.props.categories})
        )
    } 
    
    if (!this.state.edit) {
      var modalMessage = (
        React.createElement("div", null, 
          React.createElement("p", null, "Are you sure you want to delete the article ", React.createElement("em", null, this.state.title), "?"), 
          React.createElement("p", null, "This will not only remove the article, but any associated analysis that has done on it.  This cannot be undone.")
        )
      );

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

            React.createElement(WarningModal, {message: modalMessage, 
              id: this.props.id, 
              title: "Delete article?", 
              buttonText: "Delete", 
              action: this.props.deleteItem}), 

            crossForm
          )
        );
    }
    else {
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
        React.createElement(CrossWrapper, {url: cross.url, 
          title: cross.title, 
          data: cross.data, 
          id: cross.id, 
          notes: cross.notes, 
          deleteItem: this.deleteItem})
      );
    });

    return ( 
      React.createElement("div", {className: "crossList row"}, 
        React.createElement("h1", null, "Analyzed Articles"), 
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
  },deleteItem: function (id) {
    $.ajax({
      url: "http://localhost:8000/cross/articles/delete/" + id + "/",
      dataType: 'json',
      type: 'DELETE',
      cache: false,
      success: function(data) {
        // 
        var index;
        this.state.data.some(function(entry, i) {
            if (entry.id == id) {
                index = i;
                return true;
            }
        });
        this.state.data.splice(index,1);

        this.setState({data: this.state.data});
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
        React.createElement(CrossItem, {
          company: cross.company, 
          subcategory: cross.subcategory, 
          notes: cross.notes, 
          product: cross.product, 
          score: cross.score, 
          id: cross.id, 
          article_id: this.props.id})
      );
    },this);

    return (
      React.createElement("div", {className: "cross listitem col-xs-12"}, 
        React.createElement(ArticleWrapper, {
          url: this.props.url, 
          title: this.props.title, 
          notes: this.props.notes, 
          id: this.props.id, 
          deleteItem: this.deleteItem}), 
        React.createElement("div", {className: "col-xs-12 col-sm-11"}, 
          React.createElement("ul", null, 
            crossData
          )
        )
      )
    );
  }
});

var CrossItem = React.createClass ({displayName: "CrossItem",
  render: function() {
    // Color score according to whether it is positive or negative
    var scoreClass = this.props.score > 0 ? 'positive' : 'negative';
    var dlClass = 'dl-horizontal crossItem ' + scoreClass;

    return (
      React.createElement("li", null, 
        React.createElement("dl", {className: dlClass}, 
          React.createElement("dt", null, this.props.company, " ", this.props.product), 
          React.createElement("dd", null, this.props.subcategory, ": ", React.createElement("span", {className: scoreClass}, this.props.score)), 
          React.createElement("dd", null, React.createElement("span", {className: "text-muted"}, this.props.notes))
        )
      )
    );
  }
});

var CrossForm = React.createClass ({displayName: "CrossForm",
  getInitialState: function() {
    return {
      error: ''
    }
  },
  render: function() {
    console.log(this.props);
    return (
        React.createElement("div", {className: "col-xs-12 listitem"}, 

          React.createElement("h3", {className: "text-danger"}, this.state.error), 

          React.createElement("form", {method: "post", onSubmit: this.handleSubmit}, 
            React.createElement(DjangoCSRFToken, null), 

            React.createElement(FormHiddenElement, {name: "id", value: this.props.id, ref: "id"}), 

            React.createElement(FormHiddenElement, {name: "article", value: this.props.article_id, ref: "id", ref: "article"}), 

            React.createElement(FormSelectElement, {element: "company", 
                      id: this.props.id, 
                      opts: this.props.companies, 
                      headings: false}), 

            React.createElement(FormSelectElement, {element: "categories", 
                      id: this.props.id, 
                      opts: this.props.categories, 
                      headings: true, 
                      header_cat: "subcategories"}), 

            React.createElement(FormSelectElement, {element: "score", 
                      id: this.props.id, 
                      opts: this.props.categories, 
                      headings: true, 
                      header_cat: "subcategories"}), 

            React.createElement(FormTextAreaElement, {element: "notes", 
                      id: this.props.id, v: true, 
                      value: this.props.notes, ref: "notes"}), 

            React.createElement("input", {type: "submit", className: "btn btn-primary", value: "Submit"})

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

// element for forms that uses the generalized input tag
var FormInputElement = React.createClass ({displayName: "FormInputElement",
  getInitialState: function() {
    return {
      initial: this.props.value
    };
  },
  render: function() {
    var elID = this.props.element + this.props.id;

    return (
      React.createElement("div", {className: "form-group"}, 
        React.createElement("label", {htmlFor: elID}, this.props.element.toUpperCase(), ":"), 
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

// Element for Forms that uses the textarea tag
var FormTextAreaElement = React.createClass ({displayName: "FormTextAreaElement",
  render: function() {
    var elID = this.props.element + this.props.id;

    return (
      React.createElement("div", {className: "form-group"}, 
        React.createElement("label", {htmlFor: elID}, this.props.element.toUpperCase(), ":"), 
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

var FormSelectElement = React.createClass ({displayName: "FormSelectElement",
  render: function() {
    console.log(this.props);
    var elID = this.props.element + this.props.id;

    if(this.props.headings) {
      var options = this.props.opts.map(function (opt) {
        var sub = opt[this.props.header_cat].map(function (sub_opt) {
          return (
              React.createElement("option", {value: sub_opt.id}, sub_opt.name)
            );
        },this);

        return (
            React.createElement("optgroup", {label: opt.name}, 
            sub
            )
          )
      },this);
    } else {
      var options = this.props.opts.map(function (opt) {
        return (
            React.createElement("option", {value: opt.id}, opt.name)
          );
      },this);
    }

    return (
      React.createElement("div", {className: "form-group"}, 
        React.createElement("label", {htmlFor: elID}, this.props.element.toUpperCase(), ":"), 
        React.createElement("select", {className: "form-control", id: elID}, 
          React.createElement("option", {value: 0, selected: "selected"}, " -------- "), 
          options
        )
      )
    )
  }
});

// Hidden form input
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

    // Once the item has been deleted, close the modal
    $('myModal' + this.props.id).modal('toggle');
    $('body').removeClass('modal-open');
    $('.modal-backdrop').remove();
    
  },
  render: function() {
    return (
      React.createElement("div", {id: "myModal" + this.props.id, className: "modal fade", tabIndex: "-1", role: "dialog", "aria-labelledby": "myModalLabel" + this.props.id}, 
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
  React.createElement(CrossList, {url: "http://localhost:8000/cross/cross/list"}),
  document.getElementById('cross')
);