from django.contrib import admin

from .models import Course, Event, CourseCodes

class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_per_page = 100
    search_fields = ['name_en', 'name_sv', 'course_code', 'course_id', 'course_reg', 'semester', 'year', 'course_location', 'created', 'modified']
    list_display = ('name_en', 'name_sv', 'course_code', 'course_id', 'course_reg', 'semester', 'year', 'course_location', 'created', 'modified')

class CourseCodesAdmin(admin.ModelAdmin):
    model = Course
    list_per_page = 100
    search_fields = ['code', 'created', 'modified']
    list_display = ('code', 'created', 'modified')

admin.site.register(Course, CourseAdmin)
admin.site.register(Event)
admin.site.register(CourseCodes, CourseCodesAdmin)


