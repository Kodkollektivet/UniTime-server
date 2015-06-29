
from django.conf.urls import include, url
from django.contrib import admin

from timeedit.views import IndexView, CourseView, EventView
from angular.views import IndexTemplateView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),

    url(r'^a/$', IndexTemplateView.as_view(), name='a'),

    #url(r'^api/only-course-codes/$', allCouseCodesInJSON, name='only-course-codes'),
    url(r'^api/course/$', CourseView.as_view(), name='course'),
    url(r'^api/event/$', EventView.as_view(), name='event'),
    
    url(r'^admin/', include(admin.site.urls)),
]
