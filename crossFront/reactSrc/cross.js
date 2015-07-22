// ARTICLE COMPONENTS

// Component for building list of non-Cross Referenced articles
var ArticleList = React.createClass ({
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
        <ArticleWrapper 
          url={article.url} 
          title={article.title} 
          notes={article.notes} 
          id={article.id} 
          key={article.id} 
          deleteItem={this.deleteItem} 
          companies={this.state.data[2]['company']} 
          categories={this.state.data[1]['ethicscategory']} 
          addCross={this.addCross} />
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
        <h1>Unanalyzed Articles</h1>
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
  }, 
  addCross: function(data) {
    return ;
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
      add_analysis: false,
      edit: false,
      delete: false,
      title: this.props.title,
      url: this.props.url,
      notes: this.props.notes,
    };
  },
  onArticleFormSuccess: function(data) {
    this.setState({edit: false,
                   title: data['title'],
                   url: data['url'],
                   notes: data['notes']
                 });
  },
  onCrossFormSuccess: function(data) {
    this.setState({add_analysis: false});
    this.props.addCross(data);

  },
  render: function() {
    var buttons = ['add_analysis','edit'].map(function (key) {
        var classes = "btn btn-block btn-" + key;
        return (
            <button className={classes} onClick={this.handleClick.bind(this, key)} >
              {key.replace("_"," ")}
            </button>
          )
      },this);

    if(this.state.add_analysis) {
      var crossForm = (
          <CrossForm
             article_id = {this.props.id} 
             companies = {this.props.companies} 
             categories = {this.props.categories}
             id={0}
             formSuccess= {this.onCrossFormSuccess} />
        )
    } 
    
    if (!this.state.edit) {
      var modalMessage = (
        <div>
          <p>Are you sure you want to delete the article <em>{this.state.title}</em>?</p>
          <p>This will not only remove the article, but any associated analysis that has done on it.  This cannot be undone.</p>
        </div>
      );

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

            <WarningModal message={modalMessage}
              id={this.props.id}
              title="Delete article?" 
              buttonText="Delete" 
              action={this.props.deleteItem} />

            {crossForm}
          </div>
        );
    }
    else {
      var normalView = <ArticleForm 
        title={this.state.title}
        url={this.state.url}
        notes={this.state.notes}
        submitLink = {'http://localhost:8000/cross/articles/update/' + this.props.id + '/'}
        id = {this.props.id} 
        header='PUT' 
        formSuccess={this.onArticleFormSuccess} />

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
      data: [ {article: []},
              {ethicscategory: []},
              {company: []} ],
    };
  },
  render: function() {

    var crossNodes = this.state.data[0].article.map(function (cross) {
      return (
        <CrossWrapper url={cross.url} 
          title={cross.title} 
          data={cross.data} 
          id={cross.id}
          notes={cross.notes}
          deleteItem={this.deleteItem}
          companies={this.state.data[2].company}
          categories={this.state.data[1].ethicscategory } />
      );
    },this);

    return ( 
      <div className="crossList row">
        <h1>Analyzed Articles</h1>
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

var CrossWrapper = React.createClass ({
  getInitialState: function() {
    return {
      data: this.props.data
    }
  },
  render: function() {
    var crossData = this.state.data.map(function (cross) {

      return (
        <CrossItem 
          company={cross.company}
          subcategory={cross.subcategory}
          notes={cross.notes}
          product={cross.product}
          score={cross.score} 
          id={cross.id}
          article_id={this.props.id} />
      );
    },this);

    return (
      <div className="cross listitem col-xs-12">
        <ArticleWrapper 
          url={this.props.url} 
          title={this.props.title} 
          notes={this.props.notes} 
          id={this.props.id} 
          deleteItem={this.deleteItem} 
          companies={this.props.companies}
          categories={this.props.categories} 
          addCross={this.addCross} />
        <div className="col-xs-12 col-sm-11">
          <ul>
            {crossData}
          </ul>
        </div>
      </div>
    );
  },
  addCross: function(data) {
    data.company = $.grep(this.props.companies,function(v) {return v.id === data.company})[0];
    var subFlattened = []
    for (var i=0; i<this.props.categories.length;i++) {
      for (var j=0;j<this.props.categories[i].length;j++) {
        subFlatten.append(this.props.categories[i][j]);
      }
    }
    data.subcategory = $.grep(subFlattened,function(v) {return v.id === data.subcategory})[0];
    var temp = [data];
    this.setState(
      {data: this.state.data.concat(temp)}
    );
  }
});

var CrossItem = React.createClass ({
  render: function() {
    // Color score according to whether it is positive or negative
    var scoreClass = this.props.score > 0 ? 'positive' : 'negative';
    var dlClass = 'dl-horizontal crossItem ' + scoreClass;

    return (
      <li>
        <dl className={dlClass}>
          <dt>{this.props.company} {this.props.product}</dt>
          <dd>{this.props.subcategory}: <span className={scoreClass}>{this.props.score}</span></dd>
          <dd><span className="text-muted">{this.props.notes}</span></dd>
        </dl>
      </li>
    );
  }
});

var CrossForm = React.createClass ({
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
      url: 'http://localhost:8000/cross/cross/new/',
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
  getInitialState: function() {
    return {
      error: ''
    }
  },
  render: function() {
    var scoreVals = [-5,-4,-3,-2,-1,1,2,3,4,5];

    var scores = []
    for (var i=0;i < scoreVals.length; i++) {
      var score = {'name': scoreVals[i],'id': scoreVals[i]};
      scores.push(score);
    }

    return (
        <div className="col-xs-12 listitem">

          <h3 className='text-danger'>{this.state.error}</h3>

          <form method='post' onSubmit={this.handleSubmit}>
            <DjangoCSRFToken />

            <FormHiddenElement name='id' value={this.props.id} ref='id' />

            <FormHiddenElement name='article' value={this.props.article_id} ref='article' />

            <FormSelectElement element='company' 
                      id={this.props.id} 
                      opts={this.props.companies}
                      headings={false} 
                      ref='company' />

            <FormSelectElement element='categories' 
                      id={this.props.id} 
                      opts={this.props.categories}
                      headings={true} 
                      header_cat='subcategories' 
                      ref='subcategory' />

            <FormSelectElement element='score' 
                      id={this.props.id} 
                      opts={scores}
                      headings={false} 
                      ref='score' />

            <FormTextAreaElement element='notes' 
                      id={this.props.id} 
                      value={this.props.notes} ref='notes' />

            <input type='submit' className='btn btn-primary' value='Submit' />

          </form>
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

// element for forms that uses the generalized input tag
var FormInputElement = React.createClass ({
  getInitialState: function() {
    return {
      initial: this.props.value
    };
  },
  render: function() {
    var elID = this.props.element + this.props.id;

    return (
      <div className='form-group'>
        <label htmlFor={elID}>{this.props.element.toUpperCase()}:</label>
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

// Element for Forms that uses the textarea tag
var FormTextAreaElement = React.createClass ({
  render: function() {
    var elID = this.props.element + this.props.id;

    return (
      <div className='form-group'>
        <label htmlFor={elID}>{this.props.element.toUpperCase()}:</label>
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

var FormSelectElement = React.createClass ({
  render: function() {
    var elID = this.props.element + this.props.id;

    if(this.props.headings) {
      var options = this.props.opts.map(function (opt) {
        var sub = opt[this.props.header_cat].map(function (sub_opt) {
          return (
              <option value={sub_opt.id}>{sub_opt.name}</option>
            );
        },this);

        return (
            <optgroup label={opt.name}>
            {sub}
            </optgroup>
          )
      },this);
    } else {
      var options = this.props.opts.map(function (opt) {
        return (
            <option value={opt.id}>{opt.name}</option>
          );
      },this);
    }

    return (
      <div className="form-group">
        <label htmlFor={elID}>{this.props.element.toUpperCase()}:</label>
        <select className="form-control" id={elID}>
          <option value={0} selected="selected"> -------- </option>
          {options}
        </select>
      </div>
    )
  }
});

// Hidden form input
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
  handleClick: function() {
    
    this.props.action(this.props.id);

    // Once the item has been deleted, close the modal
    $('myModal' + this.props.id).modal('toggle');
    $('body').removeClass('modal-open');
    $('.modal-backdrop').remove();
    
  },
  render: function() {
    return (
      <div id={"myModal" + this.props.id} className="modal fade" tabIndex="-1" role="dialog" aria-labelledby={"myModalLabel" + this.props.id} >
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
              <button type="button" className="btn btn-primary" onClick={this.handleClick} >{this.props.buttonText}</button>
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
  <CrossList url="http://localhost:8000/cross/cross/list" />,
  document.getElementById('cross')
);