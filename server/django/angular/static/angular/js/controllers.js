var myAppController = angular.module('unitime.controllers', []);

myAppController.controller('unicontrol', function UniControl($scope, Course, Event, $scope, $cookies, $http){
    $scope.courses = {};
    $scope.events = {};

    Course.query(function(response){
        $scope.courses = response;
    });

    $scope.saveToCoockie = function(course){

        var courseObject = { 'course' : course};
        $cookies.put('courses',[]);
        var array = $cookies.get('courses');
        array.push(courseObject);
        $cookies.put('courses', array);

    };

    $scope.list = $cookies.get('courses');

  $scope.getEvents = function (course_code) {
    $http({
        url: '/api/event/',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        method: "POST",
        dataType: 'json',
        transformRequest: function(obj) {
            var str = [];
            for(var p in obj)
                str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
            return str.join("&");
        },
        data: {course: course_code}
    })
    .then(function(response) {
            $scope.services.push.apply($scope.services, data.services);
    },
    function(response) { // optional
            // failed
    });
  }

});