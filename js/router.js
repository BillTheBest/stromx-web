App.Router.map(function () {
  this.resource('files', { path: '/' });
});

App.FilesRoute = Ember.Route.extend({
  model: function () {
    return this.store.find('file');
  }
});