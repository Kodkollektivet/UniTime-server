from django.contrib import admin

from .models import Course, Event

class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_per_page = 100
    search_fields = ['name_en', 'name_sv', 'course_code', 'course_id', 'course_reg' ,'url', 'semester', 'year']
    list_display = ('name_en', 'name_sv', 'course_code', 'course_id', 'course_reg' ,'url', 'semester', 'year')

admin.site.register(Course, CourseAdmin)
admin.site.register(Event)


