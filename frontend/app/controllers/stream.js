import Ember from "ember";

export default Ember.Controller.extend({
  needs: ['application'],
  queryParams: ['view'],
  activeOutput: null,
  activeInput: null,
  view: null,
  
  viewModel: function() {
    var view = this.get('view');
    if (view === null) {
      return null;
    } else {
      var model = this.get('store').find('view', view);
      return model;
    }
  }.property('view'),
  
  isVisible: Ember.computed.equal('view', null),
  
  addConnection: function(input, output) {
    var threads = this.get('model.threads');
    var thread = threads.get('length') > 0 ? threads.objectAt(0) : null;
    var store = this.get('store');
    var model = this.get('model');
    var connection = store.createRecord('connection', {
      output: output,
      input: input,
      thread: thread,
      stream: model
    });
    
    var _this = this;
    connection.save().then(function(connection) {
      _this.transitionToRoute('connection', connection);
    });
  },
  
  removeConnection: function(connection) {
    connection.deleteRecord();
    connection.save();
  },
  
  updateValueSocket: function() {
    if (this.get('viewModel') === null) {
      this.send('disconnectFromValueSocket');
    } else {
      this.send('connectToValueSocket');
    }
  }.observes('viewModel'),

  actions: {
    save: function () {
      this.get('model.file').then(function(file) {
        file.set('saved', true);
        file.save();
      });
    },
    start: function () {
        var stream = this.get('model');
        stream.set('active', true);
        stream.save().catch(function() {
          stream.rollback();
        });
    },
    stop: function () {
        var stream = this.get('model');
        stream.set('active', false);
        stream.save();
    },
    pause: function () {
        var stream = this.get('model');
        stream.set('paused', true);
        stream.save();
    },
    resume: function () {
        var stream = this.get('model');
        stream.set('paused', false);
        stream.save();
    }
  }
});
