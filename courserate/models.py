from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        get_latest_by = 'modified'
        ordering = ('-modified', '-created')

class Rate(TimeStampedModel):
    course_code = models.CharField(max_length=50)
    course_rate = models.FloatField()
    notes = models.TextField(blank=True)
    ip = models.CharField(max_length=40)

    class Meta:
        unique_together = (('course_code', 'ip'),)