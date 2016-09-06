// /static/js/app/app.js
window.App = Ember.Application.create();
App.Router = Ember.Router.extend({ rootURL: '/b5340568bdcd46b4b5be/pa3/live'
});


App.Store = DS.Store.extend({});
App.ApplicationAdapter = DS.JSONAPIAdapter.extend({ namespace: '/b5340568bdcd46b4b5be/pa3/jsonapi/v1'
})

App.Router.map(function() {
this.route('pic', { path: '/pics/:pic_id' });
});

App.Pic = DS.Model.extend({ picurl: DS.attr('string'), prevpicid: DS.attr('string'), nextpicid: DS.attr('string'), caption: DS.attr('string'),
});

App.PicRoute = Ember.Route.extend({ model: function(params) {
var pic = this.store.findRecord('pic', params.pic_id);
return pic; },
actions: {
save: function() {
var pic = this.modelFor('pic');
var caption = this.modelFor('pic').get('caption'); this.set('caption', caption); this.modelFor('pic').save();
} },
renderTemplate: function() { this.render('pic');
} });