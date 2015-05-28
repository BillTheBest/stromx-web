import Ember from "ember";

export default Ember.Controller.extend({
  wasRemoved: false,
  actions: {
    dismiss: function () {
      if (this.get('wasRemoved')) {
        this.transitionToRoute('stream.index');
        this.set('wasRemoved', false);
      } else {
        this.transitionToRoute('view.index');
      }
    },
    remove: function () {
      var view = this.get('model');
      view.deleteRecord();
      view.save();
      this.set('wasRemoved', true);
    }
  }
});
