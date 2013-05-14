import csv
import StringIO
from tastypie.serializers import Serializer, get_type_string
from django.utils.encoding import force_unicode

import rdflib


class RDFSerializer(Serializer):
    formats = ['json', 'jsonp', 'xml', 'yaml', 'html', 'plist', 'rdf']
    content_types = {
        'json': 'application/json',
        'jsonp': 'text/javascript',
        'xml': 'application/xml',
        'yaml': 'text/yaml',
        'html': 'text/html',
        'plist': 'application/x-plist',
        'rdf': 'application/rdf+xml',
    }

    def to_rdf(self, data, options=None):
	g = rdflib.Graph()
        options = options or {}
        simple_data = self.to_simple(data, options)
	# Parse Dictionary for getting list of Objects
	for key in simple_data.keys():
		# Parse list for getting every dictionary
		if (get_type_string(simple_data[key]) == 'list'):
			for obj in simple_data[key]:
				# Parse each object's dictionary / string
				if (get_type_string(obj) == 'hash'):
					g.parse("http://www.innovagenda.com/es/event/" + str(obj["event_id"]) + "/?markFormat=rdfa", format="rdfa")
	#g.parse("/home/jon/Dropbox/Klase/PFC/Dipina/semanticmashup/semanticmashup/deustoRDFaEvents.html", format="rdfa")
        return StringIO.StringIO(g.serialize())

    def from_rdf(self, content):
        raw_data = StringIO.StringIO(content)
        data = []
        # Untested, so this might not work exactly right.
        for item in csv.DictReader(raw_data):
            data.append(item)
        return data
