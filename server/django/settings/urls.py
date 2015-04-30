from django.conf.urls import include, url
from django.contrib import admin

from timeedit.views import IndexView

urlpatterns = [
    # Examples:
    #url(r'^$', index, name='index'),
    url(r'^$', IndexView.as_view(), name='index'),
    #url(r'^events/', EventListView.as_view(), name='events'),

    #url(r'(?P<hej>\d+)/$', EventListView, name='events'),
    
    url(r'^admin/', include(admin.site.urls)),
]
