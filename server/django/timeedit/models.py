from django.db import models

class Course(models.Model):

    name_en = models.CharField(max_length=254, blank=True)  # The name of the course
    name_sv = models.CharField(max_length=254, blank=True)  # The name of the course
    syllabus_sv = models.CharField(max_length=254, blank=True)
    syllabus_en = models.CharField(max_length=254, blank=True)
    course_code = models.CharField(max_length = 10) # 1DV008
    course_id = models.CharField(max_length = 10, blank=True, unique=True) # 60380
    course_reg = models.CharField(max_length = 10, blank=True, unique=True) # ex: 67504
    course_points = models.CharField(max_length = 10, default='')
    course_location = models.CharField(max_length=254, default='')
    course_language = models.CharField(max_length=100, default='')
    course_speed = models.CharField(max_length=20, default='')
    semester = models.CharField(max_length = 2)       # HT / VT
    url = models.CharField(max_length = 254, blank=True)   # html url
    year = models.CharField(max_length = 3) 

    def __eq__(self, other):
        if self.course_code == other.course_code:
            return True
        else:
            return False

    def __unicode__(self):
        return self.course_code

class Event(models.Model):
    
    date = models.DateField()
    start_time = models.CharField(max_length = 20)
    stop_time = models.CharField(max_length = 20)
    info = models.TextField(blank=True)
    room = models.CharField(max_length = 20, blank=True)
    group = models.CharField(max_length = 100, blank=True)
    course = models.ForeignKey(Course)

    def __unicode__(self):
        return self.info

class CourseCodes(models.Model):

    code = models.CharField(max_length=10, unique=True)

    def __unicode__(self):
        return self.code
