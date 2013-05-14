import datetime
from haystack.indexes import *
from haystack import site
from website.models import *


class EventIndex(SearchIndex):
	text = CharField(document=True, use_template=True)
	#name = CharField(model_attr='name')
	event_id = IntegerField(model_attr='event_id')
	start_date = DateField(model_attr='start_date')
	finish_date = DateField(model_attr='finish_date')
	finished = BooleanField(model_attr='finished')
	localization = CharField(model_attr='localization')
	
	province = CharField(model_attr='prov')
	course_lang = CharField(model_attr='course_lang')
	activity_type = CharField(model_attr='activity_type')
	topic = CharField(model_attr='topic')
	coordinator = CharField(model_attr='coordinator')
	organizator = CharField(model_attr='organizator')

    	def index_queryset(self):
        	"""Used when the entire index for model is updated."""
        	return Event.objects.all().order_by('start_date')


site.register(Event, EventIndex)
