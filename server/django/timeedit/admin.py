from django.contrib import admin

from .models import Course, Event

class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_per_page = 100
    search_fields = ['course_code', 'course_anmalningskod', 'html_url', 'season', 'year']
    list_display = ('course_code', 'course_anmalningskod', 'html_url', 'season', 'year')

admin.site.register(Course, CourseAdmin)
admin.site.register(Event)


