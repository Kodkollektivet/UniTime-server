
from django.conf.urls import include, url
from django.contrib import admin

from timeedit.views import IndexView, CourseView, EventView, AddCourseCodeView
from timeedit.views import course_by_code, events_by_code
from angular.views import IndexTemplateView

from courserate.views import CourseRateView

urlpatterns = [
    url(r'^old/$', IndexView.as_view(), name='index'),

    url(r'^$', IndexTemplateView.as_view(), name='angular'),

    #url(r'^api/only-course-codes/$', allCouseCodesInJSON, name='only-course-codes'),
    url(r'^api/course/$', CourseView.as_view(), name='course'),
    url(r'^api/course/(?P<course_code_in>[\w-]+)/$', course_by_code , name='course_by_code'),

    url(r'^api/event/$', EventView.as_view(), name='event'),
    url(r'^api/event/(?P<course_code_in>[\w-]+)/$', events_by_code , name='events_by_code'),

    url(r'^api/rate/$', CourseRateView.as_view(), name='rate'),

    # This endpoint just adds a course code, its used to later call for new courses.
    url(r'^api/course_codes/$', AddCourseCodeView.as_view(), name='add_course_code'),
    
    url(r'^admin/', include(admin.site.urls)),
]
