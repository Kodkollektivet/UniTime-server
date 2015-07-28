from django.db import models

class Rate(models.Model):
    course_code = models.CharField(max_length=50)
    course_rate = models.FloatField()
    notes = models.TextField(blank=True)
    ip = models.CharField(max_length=40)

    class Meta:
        unique_together = (('course_code', 'ip'),)