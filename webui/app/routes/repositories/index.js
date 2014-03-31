var RepositoriesRoute = Ember.Route.extend({
  model: function() {
    return this.store.find('repository');
  }
});
export default RepositoriesRoute;
