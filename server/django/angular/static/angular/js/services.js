angular.module('unitime.services', ['ngResource'])
    .factory('Course', function($resource) {
      return $resource('/api/course/');
    })
    .factory('Event', function($resource) {
      return $resource('/api/event/');
    });
