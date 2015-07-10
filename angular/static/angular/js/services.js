
angular.module('unitime.services', ['ngResource'])
    .factory('Course', function($resource) {
      return $resource('/api/course/', {}, {
          query: { method: "GET", isArray: true }
      });
    })
    .factory('Event', function($resource) {
      return $resource('/api/event/');
    });

