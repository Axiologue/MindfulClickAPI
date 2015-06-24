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
        <ArticleWrapper url={article.url} title={article.title} notes={article.notes} />
      );
    });

    return ( 
      <div className="articleList row">
        <h1>Add New article</h1>
        <ArticleForm 
          id={0} 
          submitLink={"http://localhost:8000/cross/articles/new/"} 
          title={''}
          url={''}
          notes={''}
        />
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
  }
});

// Wrapper class for the individual non-Cross Referenced articles
var ArticleWrapper = React.createClass ({
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
            <button className={classes} onClick={this.handleClick.bind(this, key)} >
              {key}
            </button>
          )
      },this);
    
    

    return (
      <div className="article listitem col-xs-12">
        <div className="col-xs-12 col-sm-11">
          <ul>
            <li><h3>{this.props.title}</h3></li>
            <li><a href={this.props.url}>{this.props.url}</a></li>
            <li>{this.props.notes}</li>
          </ul>
        </div>
        <div className="col-sm-1 col-xs-12 text-center">
          {buttons}
        </div>
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
        console.log(xhr);

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

    var titleID = 'title' + this.props.id;
    var urlID = 'url' + this.props.id;
    var notesID = 'notes' + this.props.id;



    return (
        <div className="col-xs-12 listitem">

          <h3 className='text-danger'>{this.state.error}</h3>
          <h3 className='text-success'>{this.state.success}</h3>

          <form method='post' onSubmit={this.handleSubmit}>
            <DjangoCSRFToken />

            <div className='form-group'>
              <label for={titleID}>Title:</label>
              <input type="text" name='title' id={titleID} className="form-control" ref='title' />
            </div>

            <div className='form-group'>
              <label for={urlID}>URL:</label>
              <input type="text" name='url' id={urlID} className="form-control" ref='url' />
            </div>

            <div className='form-group'>
              <label for={notesID}>Notes:</label>
              <textarea name='notes' id={notesID} className="form-control" ref='notes' rows={3} />
            </div>

            <input type='submit' className='btn btn-primary' value='Submit' />

          </form>
        </div>
      );
  }
});

// Reusable CSRF token for forms
var DjangoCSRFToken = React.createClass ({

  render: function() {
    var csrftoken = $.cookie('csrftoken');

    return (
      <input type="hidden" name="csrfmiddlewaretoken" value={csrftoken} />
    );
  }
});


// Rendering live elements
React.render(
  <ArticleList url="http://localhost:8000/cross/articles" />,
  document.getElementById('Articles')
);