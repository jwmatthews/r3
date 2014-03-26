WebUI Prototype for RHUI 3.0
===
 * Uses Ember.js and ember-app-kit
    * [Getting started with ember-app-kit](https://github.com/stefanpenner/ember-app-kit/wiki/Getting-Started)
    * [Introduction to ember-app-kit](http://embersherpa.com/articles/introduction-to-ember-app-kit/)
    * [Deeper Introduction to ember-app-kit](http://blog.safaribooksonline.com/2013/09/18/ember-app-kit/)
    


Prerequisites:
-----
 1. Install npm
    * Fedora
      * `yum install npm`
    * OSX
      * `brew install npm`
 1. Instal Grunt CLI  
    * `npm install -g grunt-cli`
 1. Install bower
    * `npm install -g bower`
 

Getting Started:
---
 1. Run `npm install` 
 1. Run `bower install`

 
### Grunt Tasks ###

 * `grunt` - build your app and run the tests.
 * `grunt server` - run the server in development mode and automatically rebuild when files change
 * `grunt build:debug` - build your app in debug mode and output the result tmp/public directory
 * `grunt server:dist` - build your app, minify all JS and CSS and output to tmp/public directory
 * `grunt jshint` - check the javascript source code for common errors
 
 
#### Example running the development server ####
 1. `grunt server`
 1. In your browser visit ```http://0.0.0.0:8000```