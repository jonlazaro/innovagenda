# Create your views here.
from django.template import Context, loader, RequestContext
from website.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from website.forms import *
from django.core.mail import send_mail

from haystack.views import SearchView
from website.forms import EventSearchForm

import django_mobile

import rdflib
import rdflib_microdata

import urllib2


def index(request):
	if django_mobile.get_flavour(request) == 'mobile':
		return render_to_response('index.html', context_instance=RequestContext(request))
	else:
		comming_events = Event.objects.filter(finished=False).order_by('start_date')[:20]
		repeated_points = {}
		for evx in comming_events:
			evp = (evx.lat, evx.lng)
			if (evp in repeated_points):
				repeated_points[evp] += 1
			else:
				repeated_points[evp] = 1
		return render_to_response('map.html', {'comming_events': comming_events, 'repeated_points': repeated_points}, context_instance=RequestContext(request))

def mapa(request):
	comming_events = Event.objects.filter(finished=False).order_by('start_date')[:20]
	repeated_points = {}
	for evx in comming_events:
		evp = (evx.lat, evx.lng)
		if (evp in repeated_points):
			repeated_points[evp] += 1
		else:
			repeated_points[evp] = 1
	
	return render_to_response('map.html', {'comming_events': comming_events, 'repeated_points': repeated_points}, context_instance=RequestContext(request))

def calendar(request):
	return render_to_response('calendar.html', context_instance=RequestContext(request))

def apidocs(request):
	return render_to_response('apidocs.html', context_instance=RequestContext(request))

def single_event(request, eventid):
	format = request.GET.get('markFormat')
	export = request.GET.get('exportAs')	
	if export:
		g = rdflib.Graph()
		response = HttpResponse()
		if format and format == 'rdfa':
			g.parse('http://' + str(request.META['HTTP_HOST']) + "/" + request.LANGUAGE_CODE.lower() + "/event/" + str(eventid) + "/?markFormat=rdfa", format="rdfa")
		else:
			g.parse('http://' + str(request.META['HTTP_HOST']) + "/" + request.LANGUAGE_CODE.lower() + "/event/" + str(eventid), format="microdata")
		if export == "rdf":
			response = HttpResponse(g.serialize(format='xml'), mimetype='application/rdf+xml')
			response['Content-Disposition'] = 'filename=event' + str(eventid)
			if format and format == 'rdfa':
				response['Content-Disposition'] += '_rdfa.rdf'
			else:
				response['Content-Disposition'] += '_schemaorg.rdf'
		elif export == "ntriple":
			response = HttpResponse(g.serialize(format='nt'), mimetype='text/plain')
			response['Content-Disposition'] = 'filename=event' + str(eventid)
			if format and format == 'rdfa':
				response['Content-Disposition'] += '_rdfa.nt'
			else:
				response['Content-Disposition'] += '_schemaorg.nt'
		elif export == "turtle":
			response = HttpResponse(g.serialize(format='turtle'), mimetype='text/turtle')
			response['Content-Disposition'] = 'filename=event' + str(eventid)
			if format and format == 'rdfa':
				response['Content-Disposition'] += '_rdfa.ttl'
			else:
				response['Content-Disposition'] += '_schemaorg.ttl'
		elif export == "n3":
			response = HttpResponse(g.serialize(format='n3'), mimetype='text/n3;charset=utf-8')
			response['Content-Disposition'] = 'filename=event' + str(eventid)
			if format and format == 'rdfa':
				response['Content-Disposition'] += '_rdfa.n3'
			else:
				response['Content-Disposition'] += '_schemaorg.n3'
		return response
	else:
		event =  get_object_or_404(Event, event_id=eventid)
		if format and format == 'rdfa':
			return render_to_response('event.html', {'event': event, 'format': format}, context_instance=RequestContext(request))
		else:
			return render_to_response('event.html', {'event': event, 'format': ''}, context_instance=RequestContext(request))

def all_events(request):
	event_list = Event.objects.all().order_by('start_date')
	if django_mobile.get_flavour(request) == 'mobile':
		events = event_list
	else:
		paginator = Paginator(event_list, 7)

		page = request.GET.get('page')
		if not page:
			page = 1
		try:
			events = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			events = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			events = paginator.page(paginator.num_pages)
	return render_to_response('events.html', {"events": events}, context_instance=RequestContext(request))

def thanks(request):
	return render_to_response('thanks.html', context_instance=RequestContext(request))

def search(request):
	return render_to_response('search.html', context_instance=RequestContext(request))

def contact(request):
	if request.method == 'POST':
	    form = ContactForm(request.POST)
	    if form.is_valid():
		name = form.cleaned_data['name']
		message = form.cleaned_data['message']
		sender = form.cleaned_data['sender']
		recipients = ['info@innovagenda.com']

		#send_mail(subject, message, sender, recipients)
		return HttpResponseRedirect('/' + request.LANGUAGE_CODE.lower() + '/thanks/') # Redirect after POST
	else:
	    form = ContactForm() # An unbound form

	return render_to_response('contact.html', {'form': form,}, context_instance=RequestContext(request))



class CustomSearchView(SearchView):
    def __name__(self):
        return "CustomSearchView"

    def build_form(self):
        return super(CustomSearchView, self).build_form()

def customsearch(request):
	return CustomSearchView(form_class=EventSearchForm)(request)
