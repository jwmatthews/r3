var USERNAME = "admin";
var PASSWORD = "admin";

var ApplicationAdapter = DS.RESTAdapter.extend({
  namespace: 'pulp/api/v2/',
  headers: {
    "Authorization": "Basic " + btoa(USERNAME + ":" + PASSWORD) 
  },
  buildURL: function(type, id) {
    var url = this._super(type, id);
    /* We need the URL to always end with a '/' */
    if (url.slice(-1) !== '/') {
      url = url + '/';
    }
    return url;
  }
});

export default ApplicationAdapter;
