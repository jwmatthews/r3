var Router = Ember.Router.extend(); // ensure we don't share routes between all Router instances

Router.map(function() {
  this.route('component-test');
  this.route('helper-test');
  this.resource('repositories', {path: "/"}, function() {
    this.route('repository', {path: "/repositories/:repository_id"});
  });
});

export default Router;
