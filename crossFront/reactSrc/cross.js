// ARTICLE COMPONENTS

// Component for building list of non-Cross Referenced articles
var ArticleList = React.createClass ({
  getInitialState: function() {
    return {
      data: [],
    };
  },
  render: function() {
    
    var articleNodes = this.state.data.map(function (article) {
      return (
        <ArticleWrapper 
          url={article.url} 
          title={article.title} 
          notes={article.notes} 
          id={article.id} 
          key={article.id} 
          deleteItem={this.deleteItem} />
      );
    },this);

    return ( 
      <div className="articleList row">
        <h1>Add New article</h1>
        <ArticleForm 
          id={0} 
          submitLink={"http://localhost:8000/cross/articles/new/"} 
          title={''}
          url={''}
          notes={''}
          header='POST' />
        <h1>Unreferenced Articles</h1>
        {articleNodes}
      </div>
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
      url: this.props.url,
      dataType: 'json',
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
var ArticleWrapper = React.createClass ({
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
            <button className={classes} onClick={this.handleClick.bind(this, key)} >
              {key}
            </button>
          )
      },this);
    
    console.log(this.props.deleteItem);
    
    if (!this.state.cross && !this.state.edit) {
      var normalView = (
          <div className="article listitem col-xs-12">
            <div className="col-xs-12 col-sm-10">
              <ul>
                <li><h3>{this.state.title}</h3></li>
                <li><a href={this.state.url}>{this.state.url}</a></li>
                <li>{this.state.notes}</li>
              </ul>
            </div>
            <div className="col-sm-2 col-xs-12 text-center">
              {buttons}
              <button className='btn btn-block btn-delete' 
                  data-toggle="modal"
                  data-target={'#myModal' + this.props.id} 
                  type="button" >delete</button>
            </div>

            <WarningModal message={'Are you sure you want to delete the article "' + this.state.title + '"?'}
              id={this.props.id}
              title="Delete article?" 
              buttonText="Delete" 
              action={this.props.deleteItem} />
          </div>
        );
    }
    
    if (this.state.edit) {
      var normalView = <ArticleForm 
        title={this.state.title}
        url={this.state.url}
        notes={this.state.notes}
        submitLink = {'http://localhost:8000/cross/articles/update/' + this.props.id + '/'}
        id = {this.props.id} 
        header='PUT' 
        formSuccess={this.onFormSuccess} />

    }

    return (
      <div>
        {normalView}
      </div>
    );
  }
});

// Form for editing and submitting articles
var ArticleForm = React.createClass ({
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
        <div className="col-xs-12 listitem">

          <h3 className='text-danger'>{this.state.error}</h3>
          <h3 className='text-success'>{this.state.success}</h3>

          <form method='post' onSubmit={this.handleSubmit}>
            <DjangoCSRFToken />

            <FormHiddenElement name='id' value={this.props.id} ref='id' />

            <FormInputElement element='title' type='text' id={this.props.id} value={this.props.title}  ref='title' />

            <FormInputElement element='url' type='text' id={this.props.id} value={this.props.url} ref='url' />

            <FormTextAreaElement element='notes' id={this.props.id} value={this.props.notes} ref='notes' />

            <input type='submit' className='btn btn-primary' value='Submit' />

          </form>
        </div>
      );
  }
});

// CROSS REFERENCE COMPONENTS

// Component for building list of non-Cross Referenced articles
var CrossList = React.createClass ({
  getInitialState: function() {
    return {
      data: [],
    };
  },
  render: function() {
    
    var crossNodes = this.state.data.map(function (cross) {
      return (
        <CrossWrapper url={cross.url} title={cross.title} data={cross.data} />
      );
    });

    return ( 
      <div className="crossList row">
        <h1>Cross-Referenced Articles</h1>
        {crossNodes}
      </div>
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

var CrossWrapper = React.createClass ({
  render: function() {
    var crossData = this.props.data.map(function (cross) {
      return (
        <li><strong>{cross.company} {cross.product}</strong><br />
          <ul>
            <li><strong>{cross.subcategory}</strong>: {cross.score}</li>
            <li>{cross.notes}</li>
          </ul>
        </li>
      );
    });

    return (
      <div className="cross listitem col-xs-12">
        <div className="col-xs-12 col-sm-11">
          <ul>
            <li><h3>{this.props.title}</h3></li>
            <li><a href={this.props.url}>{this.props.url}</a></li>
            <li>{this.props.notes}</li>
            {crossData}
          </ul>
        </div>
      </div>
    );
  }
});

// REUSABLE COMPONENTS

// Reusable CSRF token for forms
var DjangoCSRFToken = React.createClass ({

  render: function() {
    var csrftoken = $.cookie('csrftoken');

    return (
      <input type="hidden" name="csrfmiddlewaretoken" value={csrftoken} />
    );
  }
});

var FormInputElement = React.createClass ({
  getInitialState: function() {
    return {
      initial: this.props.value
    }
  },
  render: function() {
    var elID = this.props.element + this.props.id;

    return (
      <div className='form-group'>
        <label for={elID}>{this.props.element.toUpperCase()}:</label>
        <input type={this.props.type}
          name={this.props.element} 
          id={elID} className="form-control"  
          value={this.state.initial} 
          onChange={this.onChange} />
      </div>
    );
  },
  onChange: function(e) {
    this.setState({ initial: e.target.value });
  }
});

var FormTextAreaElement = React.createClass ({
  render: function() {
    var elID = this.props.element + this.props.id;

    return (
      <div className='form-group'>
        <label for={elID}>{this.props.element.toUpperCase()}:</label>
        <textarea 
          rows={3} 
          name={this.props.element} 
          id={elID} 
          className="form-control" 
          ref={this.props.element} >{this.props.value}</textarea>
      </div>
    );
  }
});

var FormHiddenElement = React.createClass ({
  render: function() {
    return (
      <div>
        <input type='hidden' className="form-control" name={this.props.name} value={this.props.value} />
      </div>
      )
  }
})

var WarningModal = React.createClass ({
  render: function() {
    return (
      <div id={"myModal" + this.props.id} className="modal fade" tabindex="-1" role="dialog" aria-labelledby={"myModalLabel" + this.props.id} >
        <div className="modal-dialog" role="document">
          <div className="modal-content">
            <div className="modal-header">
              <button type="button" className="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
              <h4 className="modal-title" id={"myModalLabel" + this.props.id} >{this.props.title}</h4>
            </div>
            <div className="modal-body">
              <p>{this.props.message}</p>
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-default" data-dismiss="modal">Close</button>
              <button type="button" className="btn btn-primary" onClick={this.props.action(this.props.id)}>{this.props.buttonText}</button>
            </div>
          </div>
        </div>
      </div>
    );
  }
})


// Rendering live elements
React.render(
  <ArticleList url="http://localhost:8000/cross/articles" />,
  document.getElementById('articles')
);

React.render(
  <CrossList url="http://localhost:8000/cross/cross-list" />,
  document.getElementById('cross')
);