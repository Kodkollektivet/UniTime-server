
from django.conf.urls import include, url
from django.contrib import admin

from timeedit.views import IndexView, allCouseCodesInJSON, allCoursesInJSON, CourseView

from timeedit.api_handler import getAllCourseCodes

urlpatterns = [

    url(r'^$', IndexView.as_view(), name='index'),
    
    #url(r'^getall/$', getAllCourseCodes, name='getall'),
    
    url(r'^api/only-course-codes/$', allCouseCodesInJSON, name='only-course-codes'),
    url(r'^api/course/$', CourseView.as_view(), name='courses'),

    url(r'^admin/', include(admin.site.urls)),
]
