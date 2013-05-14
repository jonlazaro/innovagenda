from django import forms
from haystack.forms import SearchForm
from website.models import *


class EventSearchForm(SearchForm):
    start_date = forms.DateField(required=False)
    event_id = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
	super(EventSearchForm,self).__init__(*args,**kwargs)
	prov_choices = Province.objects.all()
	prov_tuples = tuple(([(c.id, c.name) for c in prov_choices]))
	self.fields['province'] = forms.ChoiceField(choices=prov_tuples, required=False)

	lang_choices = Language.objects.all()
	lang_tuples = tuple(([(c.id, c.name) for c in lang_choices]))
	self.fields['lang'] = forms.ChoiceField(choices=lang_tuples, required=False)

	activ_choices = ActivityType.objects.all()
	activ_tuples = tuple(([(c.id, c.name) for c in activ_choices]))
	self.fields['activ'] = forms.ChoiceField(choices=activ_tuples, required=False)

	topic_choices = Topic.objects.all()
	topic_tuples = tuple(([(c.id, c.name) for c in topic_choices]))
	self.fields['topic'] = forms.ChoiceField(choices=topic_tuples, required=False)

	agency_choices = Agency.objects.all()
	agency_tuples = tuple(([(c.id, c.name) for c in agency_choices]))
	self.fields['coord'] = forms.ChoiceField(choices=agency_tuples, required=False)
	self.fields['org'] = forms.ChoiceField(choices=agency_tuples, required=False)
    
    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(EventSearchForm, self).search()

	# Check to see if a start_date was chosen.
	if self.is_valid():	
		if self.cleaned_data['start_date']:
		    sqs = sqs.filter(start_date__gte=self.cleaned_data['start_date'])
	
		if self.cleaned_data['event_id']:
		    sqs = sqs.filter(event_id__exact=self.cleaned_data['event_id'])

		if self.cleaned_data['province']:
		    pass#sqs = sqs.filter(prov__id=self.cleaned_data['province'])

		if self.cleaned_data['lang']:
		    pass#sqs = sqs.filter(course_lang__id=self.cleaned_data['lang'])
	
		if self.cleaned_data['activ']:
		    pass#sqs = sqs.filter(activity_type__id=self.cleaned_data['activ'])

		if self.cleaned_data['topic']:
		    pass#sqs = sqs.filter(topic__id=self.cleaned_data['topic'])
	
		if self.cleaned_data['coord']:
		    pass#sqs = sqs.filter(coordinator__id=self.cleaned_data['coord'])

		if self.cleaned_data['org']:
		    pass#sqs = sqs.filter(organizator__id=self.cleaned_data['org'])
		
	return sqs


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    sender = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
