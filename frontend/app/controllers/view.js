import Ember from "ember";

import InputObserver from 'stromx-web/models/input-observer';

export default Ember.ObjectController.extend({
  isEditingName: false,

  actions: {
    saveName: function() {
      var model = this.get('model');
      model.save();
      this.set('isEditingName', false);
    },

    rename: function() {
      this.set('isEditingName', true);
    },

    remove: function () {
        var view = this.get('model');
        view.deleteRecord();
        view.save();
    }
  },

  parameterObservers: Ember.computed.alias('observers'),

  inputObservers: Ember.computed.filter('observers', function(observer) {
    return observer instanceof InputObserver;
  }),

  svgSorting: ['zvalue:incr'],
  svgObservers: Ember.computed.sort('observers', 'svgSorting'),
});
