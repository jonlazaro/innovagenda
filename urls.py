from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from tastypie.api import Api
from website.api.api import ActivityTypeResource, TopicResource, AgencyResource, ProvinceResource, LanguageResource, EventResource

admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(ActivityTypeResource())
v1_api.register(TopicResource())
v1_api.register(AgencyResource())
v1_api.register(ProvinceResource())
v1_api.register(LanguageResource())
v1_api.register(EventResource())

urlpatterns = patterns('',
    # Innovagenda URLs
    (r'^$', 'website.views.index'),
    (r'^map/$', 'website.views.mapa'),
    (r'^events/$', 'website.views.all_events'),
    (r'^calendar/$', 'website.views.calendar'),
    #(r'^search/$', 'website.views.search'),
    (r'^search/', 'website.views.customsearch'),#include('haystack.urls')),
    (r'^event/(?P<eventid>\d+)/$', 'website.views.single_event'),
    (r'^contact/$', 'website.views.contact'),
    (r'^thanks/$', 'website.views.thanks'),
    (r'^apidocs/$', 'website.views.apidocs'),

    # Admin
    (r'^admin/', include(admin.site.urls)),

    # Rosetta
    url(r'^rosetta/', include('rosetta.urls')),

    # API
    (r'^api/', include(v1_api.urls)),

    # Localeurl
    (r'^localeurl/', include('localeurl.urls')),

    # Static content
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
)
