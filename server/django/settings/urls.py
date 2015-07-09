
from django.conf.urls import include, url
from django.contrib import admin

from timeedit.views import IndexView, CourseView, EventView
from angular.views import IndexTemplateView

from courserate.views import CourseRateView

urlpatterns = [
    url(r'^old/$', IndexView.as_view(), name='index'),

    url(r'^$', IndexTemplateView.as_view(), name='angular'),

    #url(r'^api/only-course-codes/$', allCouseCodesInJSON, name='only-course-codes'),
    url(r'^api/course/$', CourseView.as_view(), name='course'),
    url(r'^api/event/$', EventView.as_view(), name='event'),

    url(r'^api/rate/$', CourseRateView.as_view(), name='rate'),
    
    url(r'^admin/', include(admin.site.urls)),
]
