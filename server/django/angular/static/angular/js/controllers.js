var myAppController = angular.module('unitime.controllers', []);

myAppController.controller('unicontrol', function UniControl($scope, Course, Event, $scope, $cookies, $http){
    $scope.courses = [];
    $scope.events = [];
    $scope.selected_courses = [];
    $scope.message = "";
    $scope.course_info = "satan";
    $scope.cookie_accepted;
    $scope.date = new Date();

    $scope.acceptCookieFunction = function(){
        $scope.cookie_accepted = 't';
        $cookies.put('accept_cookies', $scope.cookie_accepted);
    };

    $scope.timediff = function(start_datetime){
        var now = new Date();
        return moment.utc(moment(start_datetime).diff(moment(now))).format("mm")
    };

    // Init method
    $scope.init = function(){
        $scope.selected_courses = $cookies.getObject("courses");
         if(typeof $scope.selected_courses === 'undefined'){
             $scope.selected_courses = [];
         }
         else{
             angular.forEach($scope.selected_courses, function(course){
                 $scope.getEvents(course['course_code']);
             });
         }
        // Get accept cookies
        if ($cookies.get('accept_cookies') === 't'){
            $scope.cookie_accepted = 't';
        }
        else {
            $scope.cookie_accepted = 'f';
        }
    };

    Course.query(function(response){
        for (var i = 0 ; i < response.length ; i++){
            $scope.courses.push(response[i]);
        }
        //$scope.courses = response.data;
    });


    $scope.courseDetail = function(courseIn){
        $scope.course_info = _.filter($scope.selected_courses, function(course){
            if (course.course_code === courseIn.course_code){
                return course;
            }
        });
        $scope.course_info = $scope.course_info[0];
    };

    $scope.getCourse = function (course_code) {
        $cookies.put('accept_cookies', 't');
        $scope.cookie_accepted = 't';
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

                    // If course is already added to selected_courses list
                    if(_.contains(_.map($scope.selected_courses, function(course){
                            return course.course_code;
                        }), response.data[i]['course_code'])){
                    }
                    else{
                        $scope.selected_courses.push(response.data[i]); // Push course obj to selected list
                        $scope.getEvents(response.data[i]['course_code']); // Get events
                        var now = new Date(); // today date
                        var exp = new Date(now.getFullYear()+1, now.getMonth(), now.getDate()); // cookie expire date, 1 year
                        $cookies.putObject('courses', $scope.selected_courses, {expires: exp}); // Store in cookie
                        $scope.message = response.data[i]['name_en']+" added!";
                        openAlertMessage();
                        closeAlertMessage();

                    }
                }


            },
            function(response) { // optional
                //alert(response); // ERROR
            });
    };

    $scope.removeCourse = function(course_in){
        $scope.selected_courses.splice($scope.selected_courses.indexOf(course_in), 1);

        // Remove events connected to removed course
        angular.forEach($scope.events, function(course){
            if (course_in['course_code'] == course['course_code']){
                $scope.events = _.without($scope.events, course);

            }
        });
        $('#courseModal').modal('hide'); // close modal when course is deleted
        $cookies.putObject('courses', $scope.selected_courses); // Store in cookie
    };


    $scope.getEvents = function (course_code) {
        $('#ajaxloader').show();
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
                    var d = response.data[i]['startdate'].split('-');
                    var t = response.data[i]['starttime'].split(':');
                    var date = new Date(d[0], d[1], d[2], t[0], t[1]);
                    var date_now = new Date();
                    //console.log(date_now);
                    response.data[i]['start_datetime'] = date;
                    response.data[i]['day'] = moment(response.data[i]['startdate']).format('dddd');
                    //response.data[i]['until'] = (date-date_now)/(24*3600*1000);
                    //console.log(response.data[i]['start_datetime'].toLocaleString());
                    //console.log(response.data[i]);
                    $scope.events.push(response.data[i]);
                }
                $('#ajaxloader').hide();
                $('#date_today').show();
                $('#filterCoursesForm').show();
            },
            function(response) { // optional
                // ERROR
            });
    };

    $scope.rateCourse = function(courseIn, course_code, course_rate, notes){
        $('#ajaxloader').show();
        $scope.removeCourse(courseIn);
        console.log(courseIn);
        $http({
            url: '/api/rate/',
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
            data: {course_code: course_code, course_rate: course_rate, notes: notes}
        })
            .then(function(response) {
                $('#ajaxloader').hide();

                console.log(response.data);
            },
            function(response) { // optional
                // ERROR
                $('#ajaxloader').hide();
                console.log(response);
            });
    };

    // Calling init method
    $scope.init();

});