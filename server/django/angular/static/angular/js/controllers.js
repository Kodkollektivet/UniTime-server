var myAppController = angular.module('unitime.controllers', []);

myAppController.controller('unicontrol', function UniControl($scope, Course, Event, $scope, $cookies, $http){
    $scope.courses = [];
    $scope.events = [];
    $scope.selected_courses = [];

    Course.query(function(response){
        for (var i = 0 ; i < response.length ; i++){
            $scope.courses.push(response[i]);
        }
        //$scope.courses = response.data;
    });

    $scope.saveToCoockie = function(course){

        var courseObject = { 'course' : course};
        $cookies.put('courses',[]);
        var array = $cookies.get('courses');
        array.push(courseObject);
        $cookies.put('courses', array);

    };

    $scope.list = $cookies.getObject('courses');

    $scope.getCourse = function (course_code) {
        $http({
            url: '/api/course/',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            method: "POST",
            dataType: 'json',
            async: false,
            transformRequest: function(obj) {
                var str = [];
                for(var p in obj)
                    str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
                return str.join("&");
            },
            data: {course: course_code}
        })
            .then(function(response) {
                for ( var i = 0 ; i < response.data.length ; i++){
                    $scope.selected_courses.push(response.data[i]);
                    $scope.getEvents(response.data[i]['course_code']);
                    $cookies.putObject('courses', response.data[i]['course_code']);
                }
            },
            function(response) { // optional
                alert(response);
            });
    };

    $scope.removeCourse = function(course_in){
        $scope.selected_courses.splice($scope.selected_courses.indexOf(course_in), 1);

        angular.forEach($scope.events, function(course){
            //console.log(course_in['course_code']);
            //console.log(course['course_code']);
            if (course_in['course_code'] == course['course_code']){
                //console.log("LIKA");
                $scope.events = _.without($scope.events, course);
            }
        });
        /*
        for (var i = 0; i < $scope.events.length ; i++){

            if ($scope.events[i]['course_code'].localeCompare(course['course_code']) == 0){

                console.log($scope.events[i]['course_code']);
                console.log(course['course_code']);
                console.log("");
                var index = $scope.events[i];
                console.log(index);
                $scope.events.splice($scope.events.indexOf($scope.events[i],1));

            }
        }
        */
    };

    $scope.getEvents = function (course_code) {
        $http({
            url: '/api/event/',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            method: "POST",
            dataType: 'json',
            async: false,
            transformRequest: function(obj) {
                var str = [];
                for(var p in obj)
                    str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
                return str.join("&");
            },
            data: {course: course_code}
        })
            .then(function(response) {
                for ( var i = 0 ; i < response.data.length ; i++){
                    $scope.events.push(response.data[i]);
                }
            },
            function(response) { // optional
                // failed
            });
    }

});