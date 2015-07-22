unitime project



API Endpoints

HEAD
/api/course/

Returns: Length of all course objects stored in db.


GET
/api/course/

Returns: List with course objects thats stored in db.
Objects has attributes: course_code, name_sv, name_en


POST
/api/course/
{'course':'1DV008'}

Returns a single object in a list.
Object has attributes: syllabus_en, semester, year, course_id, name_en, name_sv, course_location,
                       course_language, course_points, syllabus_sv, url, course_speed, course_code


GET
/api/course/[1DV008]

Returns a single object in a list.
Object has attributes: syllabus_en, semester, year, course_id, name_en, name_sv, course_location,
                       course_language, course_points, syllabus_sv, url, course_speed, course_code


POST
/api/event/
{'course':'1DV008'}

Returns a list of events objects.
Object has attributes: info, startdate, name_sv, room, starttime, name_en, course_code, endtime,
                       teacher, desc


GET
/api/event/[1BD105]

Returns a list of events objects.
Object has attributes: info, startdate, name_sv, room, starttime, name_en, course_code, endtime,
                       teacher, desc
