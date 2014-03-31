var RepositoriesRepositoryRoute = Ember.Route.extend({
  model: function(repository) {
    return this.store.find('repository', repository.repository_id);
  }
});
export default RepositoriesRepositoryRoute;