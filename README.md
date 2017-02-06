<h1>OLD REPO!</h1>
<h1>New repo is here: https://github.com/Kodkollektivet/unitime-api</h1>

<h1>UniTime server</h1>
<h2>http://unitime.se (AngularJS app not maintained!)</h2>
<h3>This is out "main" server in the UniTime project.</h3>
<p>This server gets data from TimeEdit and publish the data with a JSON Rest API.</p>
<p>We Rest API is consumed by a native Android app and a Ionic webapp that is developed for iOS.</p>
<p>The server also publish a AngularJS web app.</p>
<p>The AngularJS webapp is at the moment not maintained</p>
<br>
<p>If you would like to contrib to this project, we would be more than happy</p>
<br>
<br>


<h2>API Endpoints</h2>
<br>
<p>HEAD</p>
<p>/api/course/</p>
<p>Returns: Length of all course objects stored in db.</p>

<br>

<p>GET</p>
<p>/api/course/</p>

</p>Returns: List with course objects thats stored in db.
Objects has attributes: course_code, name_sv, name_en</p>

<br>
<p>POST</p>
<p>/api/course/</p>
<p>{'course':'1DV008'}</p>
<p>
Returns a single object in a list.
Object has attributes: syllabus_en, semester, year, course_id, name_en, name_sv, course_location,
                       course_language, course_points, syllabus_sv, url, course_speed, course_code</p>

<br>
<p>GET</p>
<p>/api/course/[1DV008]</p>
<p>Returns a single object in a list.
Object has attributes: syllabus_en, semester, year, course_id, name_en, name_sv, course_location,
                       course_language, course_points, syllabus_sv, url, course_speed, course_code</p>

<br>
<p>POST</p>
<p>/api/event/</p>
<p>{'course':'1DV008'}</p>
<p>Returns a list of events objects.
Object has attributes: info, startdate, name_sv, room, starttime, name_en, course_code, endtime,
                       teacher, desc</p>

<br>
<p>GET</p>
<p>/api/event/[1BD105]</p>
<p>Returns a list of events objects.
Object has attributes: info, startdate, name_sv, room, starttime, name_en, course_code, endtime,
                       teacher, desc</p>
