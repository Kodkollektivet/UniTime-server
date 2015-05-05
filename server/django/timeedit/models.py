from django.db import models

class Course(models.Model):

    name = models.CharField(max_length=254, blank=True)  # The name of the course
    code = models.CharField(max_length = 10, unique=True) # 1DV008
    reg_code = models.CharField(max_length = 10, blank=True) # ex: 67504
    semester = models.CharField(max_length = 2)       # HT / VT
    url = models.CharField(max_length = 254)   # html url
    year = models.CharField(max_length = 3) 

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
    
