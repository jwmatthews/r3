/*
export default DS.FixtureAdapter.extend();
*/

var USERNAME = "admin";
var PASSWORD = "admin";

var ApplicationAdapter = DS.RESTAdapter.extend({
  namespace: 'pulp/api/v2/',
  headers: {
    "Authorization": "Basic " + btoa(USERNAME + ":" + PASSWORD) 
  },
  pathForType: function(type) {
    console.log("pathForType invoked with " + type);
    if (type === "repository") {
      return "repositories/";
    }
    else {
      var decamelized = Ember.String.decamelize(type);
      return Ember.String.pluralize(decamelized);
    }
  }
});

export default ApplicationAdapter;
