Ember.Inflector.inflector.irregular('repository', 'repositories');

var Repository = DS.Model.extend({
  _href: DS.attr('string'),
  _ns: DS.attr('string'),
  description: DS.attr('string'),
  display_name: DS.attr('string')
});
export default Repository;