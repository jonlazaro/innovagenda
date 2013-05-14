from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS

from django.conf.urls.defaults import url

from website.models import *
from website.api import RDFSerializer

class ActivityTypeResource(ModelResource):
	class Meta:	
		queryset = ActivityType.objects.all()
	        excludes = ['id', 'name_es', 'name_eu']
	        include_resource_uri = False
		allowed_methods = ['get']
	
	def dehydrate(self, bundle):
		lang = bundle.request.GET.get('lang', 'both')
		if lang == 'es':
			bundle.data['name_es'] = bundle.obj.name_es
		elif lang == 'eu':
			bundle.data['name_eu'] = bundle.obj.name_eu
		else:
			bundle.data['name_es'] = bundle.obj.name_es
			bundle.data['name_eu'] = bundle.obj.name_eu
		return bundle

class TopicResource(ModelResource):
	class Meta:	
		queryset = Topic.objects.all()
	        excludes = ['id', 'name_es', 'name_eu']
	        include_resource_uri = False
		allowed_methods = ['get']
	
	def dehydrate(self, bundle):
		lang = bundle.request.GET.get('lang', 'both')
		if lang == 'es':
			bundle.data['name_es'] = bundle.obj.name_es
		elif lang == 'eu':
			bundle.data['name_eu'] = bundle.obj.name_eu
		else:
			bundle.data['name_es'] = bundle.obj.name_es
			bundle.data['name_eu'] = bundle.obj.name_eu
		return bundle

class AgencyResource(ModelResource):
	class Meta:	
		queryset = Agency.objects.all()
	        excludes = ['id']
	        include_resource_uri = False
		allowed_methods = ['get']

class ProvinceResource(ModelResource):
	class Meta:	
		queryset = Province.objects.all()
	        excludes = ['id', 'name_es', 'name_eu']
	        include_resource_uri = False
		allowed_methods = ['get']
	
	def dehydrate(self, bundle):
		lang = bundle.request.GET.get('lang', 'both')
		if lang == 'es':
			bundle.data['name_es'] = bundle.obj.name_es
		elif lang == 'eu':
			bundle.data['name_eu'] = bundle.obj.name_eu
		else:
			bundle.data['name_es'] = bundle.obj.name_es
			bundle.data['name_eu'] = bundle.obj.name_eu
		return bundle

class LanguageResource(ModelResource):
	class Meta:	
		queryset = Language.objects.all()
	        excludes = ['id', 'name_es', 'name_eu']
	        include_resource_uri = False
		allowed_methods = ['get']
	
	def dehydrate(self, bundle):
		lang = bundle.request.GET.get('lang', 'both')
		if lang == 'es':
			bundle.data['name_es'] = bundle.obj.name_es
		elif lang == 'eu':
			bundle.data['name_eu'] = bundle.obj.name_eu
		else:
			bundle.data['name_es'] = bundle.obj.name_es
			bundle.data['name_eu'] = bundle.obj.name_eu
		return bundle


class EventResource(ModelResource):
	activity_type = fields.ToOneField('website.api.api.ActivityTypeResource',
                                 'activity_type', full=True)
	topic = fields.ToOneField('website.api.api.TopicResource',
                                 'topic', full=True)
	coordinator = fields.ToOneField('website.api.api.AgencyResource',
                                 'coordinator', full=True)
	organizator = fields.ToOneField('website.api.api.AgencyResource',
                                 'organizator', full=True)
	province = fields.ToOneField('website.api.api.ProvinceResource',
                                 'prov', full=True)	
	course_lang = fields.ToOneField('website.api.api.LanguageResource',
                                 'course_lang', full=True)

	class Meta:
		queryset = Event.objects.all()
		filtering = {
		    "name_es": ALL,
		    "name_eu": ALL,
		    "start_date": ALL,
		    "finish_date": ALL,
		}
		allowed_methods = ['get']
		excludes = ['id', 'inserted_date', 'finished', 'duration', 'description_es', 'description_eu', 'summary_es', 'summary_eu', 'localization_es', 'localization_eu', 'url_es', 'url_eu']
		serializer = RDFSerializer.RDFSerializer()

	def dehydrate(self, bundle):
		lang = bundle.request.GET.get('lang', 'both')
		if lang == 'es':
			#bundle.data['name_es'] = bundle.obj.name_es
			#bundle.data['description_es'] = bundle.obj.description_es
			bundle.data['summary_es'] = bundle.obj.summary_es
			bundle.data['localization_es'] = bundle.obj.localization_es
			bundle.data['url_es'] = bundle.obj.url_es
		elif lang == 'eu':
			#bundle.data['name_eu'] = bundle.obj.name_eu
			#bundle.data['description_eu'] = bundle.obj.description_eu
			bundle.data['summary_eu'] = bundle.obj.summary_eu
			bundle.data['localization_eu'] = bundle.obj.localization_eu
			bundle.data['url_eu'] = bundle.obj.url_eu
		else:
			#bundle.data['name_es'] = bundle.obj.name_es
			#bundle.data['name_eu'] = bundle.obj.name_eu
			#bundle.data['description_es'] = bundle.obj.description_es
			#bundle.data['description_eu'] = bundle.obj.description_eu
			bundle.data['summary_es'] = bundle.obj.summary_es
			bundle.data['summary_eu'] = bundle.obj.summary_eu
			bundle.data['localization_es'] = bundle.obj.localization_es
			bundle.data['localization_eu'] = bundle.obj.localization_eu
			bundle.data['url_es'] = bundle.obj.url_es
			bundle.data['url_eu'] = bundle.obj.url_eu
		return bundle

	def override_urls(self):
		return [
		    url(r"^(?P<resource_name>%s)/(?P<event_id>\d+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
		]
