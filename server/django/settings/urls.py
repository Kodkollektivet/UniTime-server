from django.conf.urls import include, url
from django.contrib import admin

from timeedit.views import IndexView, allCouseCodesInJSON

from timeedit.api_handler import getAllCourseCodes

urlpatterns = [
    # Examples:
    #url(r'^$', index, name='index'),
    url(r'^$', IndexView.as_view(), name='index'),
    #url(r'^getall/$', getAllCourseCodes, name='getall'),
    url(r'^api/only-course-codes/$', allCouseCodesInJSON, name='json'),
    #url(r'(?P<hej>\d+)/$', EventListView, name='events'),
    
    url(r'^admin/', include(admin.site.urls)),
]
