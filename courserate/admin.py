from django.contrib import admin

from .models import Rate



class RateAdmin(admin.ModelAdmin):
    model = Rate
    list_per_page = 100
    search_fields = ['course_code', 'course_rate', 'notes']
    list_display = ('course_code', 'course_rate', 'notes')

admin.site.register(Rate, RateAdmin)