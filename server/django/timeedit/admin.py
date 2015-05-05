from django.contrib import admin

from .models import Course, Event

class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_per_page = 100
    search_fields = ['name', 'code', 'reg_code', 'url', 'semester', 'year']
    list_display = ('name', 'code', 'reg_code', 'url', 'semester', 'year')

admin.site.register(Course, CourseAdmin)
admin.site.register(Event)


