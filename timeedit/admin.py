from django.contrib import admin

from .models import Course, Event, CourseCodes

class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_per_page = 100
    search_fields = ['name_en', 'name_sv', 'course_code', 'course_id', 'course_reg', 'url', 'semester', 'year', 'course_location']
    list_display = ('name_en', 'name_sv', 'course_code', 'course_id', 'course_reg', 'url', 'semester', 'year', 'course_location')

class CourseCodesAdmin(admin.ModelAdmin):
    model = Course
    list_per_page = 100
    search_fields = ['code', 'created', 'modified']
    list_display = ('code', 'created', 'modified')

admin.site.register(Course, CourseAdmin)
admin.site.register(Event)
admin.site.register(CourseCodes, CourseCodesAdmin)


