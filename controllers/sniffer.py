# encoding: utf-8

import feedparser
import urllib
import urllib2
import re
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
from datetime import time, date, timedelta, datetime
from django.utils.encoding import force_unicode

# Google Data API Imports
try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import gdata.calendar.data
import gdata.calendar.client
import gdata.acl.data
import atom
import getopt
import sys
import string
import time as time_tools

from website.models import *

from gcalendar_passwords import gcalendaruser, gcalendarpassword


def sniff():
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor) #Cookie enable url opener
	rss_urls = {
		"http://www.euskadinnova.net/modulos/RSSGenerar.aspx?language=es&tematica=2&tipo=2": "Innovación Tecnológica",
		"http://www.euskadinnova.net/modulos/RSSGenerar.aspx?language=es&tematica=3&tipo=2": "Innovación Social",
		"http://www.euskadinnova.net/modulos/RSSGenerar.aspx?language=es&tematica=4&tipo=2": "Transformación Empresarial",
		"http://www.euskadinnova.net/modulos/RSSGenerar.aspx?language=es&tematica=5&tipo=2": "Enpresa Digitala",
	}

	#re pattern for getting event ID
	pat_evid = re.compile('.*/(\d+)\.aspx')
	#re pattern for getting start and finish dates
	pat_dates = re.compile('\d{2}/\d{2}/\d{4}')
	#re pattern for integers
	pat_digits = re.compile('\d+')
	#re pattern for floats
	pat_floats = re.compile('\d+,\d+')
	#re pattern for getting start and finish hours
	pat_hours = re.compile('\d+:\d+')

	for rss_url in rss_urls:	
		rss = feedparser.parse(rss_url)

		#General data from rss
		#---------------------

		#Topic
		topic_str = rss_urls[rss_url]

		for entry in rss.entries:
			#event_id		
			evid = pat_evid.split(entry.link)[1]
			print "...EVENT " + str(evid) + " parsing..."
			#If the event is in the DB, no parsing
			try:
				event = Event.objects.get(event_id = evid)
				print "EVENT " + str(evid) + " already in DB" + "\n"
			except Event.DoesNotExist:
				url_es = "http://www.euskadinnova.net/es/enpresa-digitala/agenda/x/" + str(evid)  + ".aspx"
				url_eu = "http://www.euskadinnova.net/eu/enpresa-digitala-eu/agenda/x/" + str(evid)  + ".aspx"

				#Parse HTML
				response = opener.open(url_es)
				data = response.read()
				soup_es = BeautifulSoup(data)
				soup_es.prettify()

				response = opener.open(url_eu)
				data = response.read()
				soup_eu = BeautifulSoup(data)
				soup_eu.prettify()
		
				#name
				name_es = soup_es.find('span', id="ctl09_ltrTitulo").contents[0]
				name_eu = soup_eu.find('span', id="ctl09_ltrTitulo").contents[0]

				#dates
				dates = pat_dates.findall(entry.title)
				dateparts = pat_digits.findall(dates[0])
				start_date = date(int(dateparts[2]), int(dateparts[1]), int(dateparts[0]))
		
				try:
					dateparts = pat_digits.findall(dates[1])
					finish_date = date(int(dateparts[2]), int(dateparts[1]), int(dateparts[0]))
				except IndexError:
					finish_date = start_date

				#hours
				try:
					hours = pat_hours.findall(soup_es.find('li', id="ctl09_div_horario").next.next.next)
					hourparts = pat_digits.findall(hours[0])
					start_hour = time(int(hourparts[0]), int(hourparts[1]))
					hourparts = pat_digits.findall(hours[1])
					finish_hour = time(int(hourparts[0]), int(hourparts[1]))
				except AttributeError:
					start_hour = None
					finish_hour = None 
				except IndexError:
					finish_hour = start_hour

				#duration
				try:
					duration = int(pat_digits.findall(soup_es.find('li', id="ctl09_div_duracion").find('strong').contents[0])[0])
				except:
					duration = None

				#price
				try:
					pricestr = pat_floats.findall(soup_es.find('li', id="ctl09_div_precio").find('strong').contents[0])[0]
					if (pricestr in ['Gratuito', 'Gratis']):
						price = 0
					else:					
						price = float(pricestr.replace(',', '.'))
				except:
					price = None
		
				#description
				desc_es = str(soup_es.find('div', id="ctl09_div_contenido").find('div'))
				desc_eu = str(soup_eu.find('div', id="ctl09_div_contenido").find('div'))

				s = BeautifulSoup(force_unicode(desc_es))
				desc_es = ''.join(s.findAll(text=True))
				s = BeautifulSoup(force_unicode(desc_eu))
				desc_eu = ''.join(s.findAll(text=True))

				#summary
				summary_es = soup_es.find("meta", id="metaDcDescription")["content"]
				summary_eu = soup_eu.find("meta", id="metaDcDescription")["content"]
				#summary_es = soup_es.find('div', id="ctl09_div_descripcion").find('div').string
				#summary_eu = soup_eu.find('div', id="ctl09_div_descripcion").find('div').string

				#teacher
				try:
					teacher = soup_es.find('li', id="ctl09_div_impartidoPor").find('strong').contents[0]
				except:
					teacher = None

				#url
				url_es = "http://www.euskadinnova.net" + str(soup_es.form['action'])
				url_eu = "http://www.euskadinnova.net" + str(soup_eu.form['action'])

				#GEOLOCALIZATION
				#Get Address
				place_es = soup_es.find('li', id="ctl09_div_localizacion").find('strong').contents[0]
				place_eu = soup_eu.find('li', id="ctl09_div_localizacion").find('strong').contents[0]
				place = geolocalize(place_es, place_eu)

				#FOREIGN KEYS
				#language
				lang_str = soup_es.find('li', id="ctl09_div_idiomaImparticion").find("strong").contents[0]

				#activity_type
				act_str = soup_es.find('span', id="ctl09_ltrTipoEvento").contents[0]				

				#coordinator
				coord_str = soup_es.find('li', id="ctl09_div_agenciaCoordinadora").find('strong').contents[0]
		
				#organizator
				org_str = soup_es.find('li', id="ctl09_div_organizador").find('strong').contents[0]

				#CREATE THE EVENT WITH ALL PARSED DATA

				#save geolocalization in DB
		

				event = Event()
				event.event_id = evid
				event.name_es = str(name_es)
				event.name_eu = str(name_eu)
				event.start_date = start_date
				event.finish_date = finish_date
				event.start_hour = start_hour
				event.finish_hour = finish_hour
				event.duration = duration
				event.price = price
				event.description_es = str(desc_es)
				event.description_eu = str(desc_eu)
				event.summary_es = summary_es
				event.summary_eu = summary_eu
				event.teacher = str(teacher)
				event.url_es = str(url_es)
				event.url_eu = str(url_eu)
				event.localization_es = place.name_es
				event.localization_eu = place.name_eu
				event.address = place.address
				event.lat = place.lat
				event.lng = place.lng
				event.prov = place.prov

				#Set data from foreign keys
				event.set_foreign_data(str(act_str), str(topic_str), str(coord_str), str(org_str), str(lang_str))
		
				#Insert in Google Calendar
				gcalurl_es, gcalurl_eu = insertInGCalendar(event=event)
				event.gcalendar_url_es = gcalurl_es
				event.gcalendar_url_eu = gcalurl_eu

				#Save it in database
				event.save()

				print "EVENT " + str(event.event_id) + " OK!" + "\n" + event.url + "\n"

def get_province(prov):
	if (prov in ['Vizcaya', 'Bizkaia']):
		return Province.objects.get(name_eu = 'Bizkaia')
	elif (prov in ['Guipuzcoa', 'Guipúzcoa', 'Gipuzkoa']):
		return Province.objects.get(name_eu = 'Gipuzkoa')
	elif (prov in ['Álava', 'Alava', 'Araba']):
		return Province.objects.get(name_eu = 'Araba')
	else:
		return Province.objects.get(name_es = 'Otras')

def geolocalize(address_es, address_eu):
	#re pattern for getting postal code
	pat_cp = re.compile('\d{5}')
	gmaps_url = "http://maps.google.com/maps/api/geocode/xml?address="
	a = str(address_es).lower()
	place = None
	if (a.find("parque tecnol") != -1):
		if (a.find("zamudio") != -1) or (a.find("bizkaia") != -1) or (a.find("vizcaya") != -1):
			place = Place.objects.get(name_es = "Parque Tecnológico de Zamudio")
		elif (a.find("guipuzcoa") != -1) or (a.find("gipuzkoa") != -1) or (a.find("guipúzcoa") != -1) or (a.find("donosti") != -1) or (a.find("san seb") != -1):
			place = Place.objects.get(name_es = "Parque Tecnológico de San Sebastián")
		elif (a.find("álava") != -1) or (a.find("alava") != -1) or (a.find("araba") != -1) or (a.find("miñano") != -1):
			place = Place.objects.get(name_es = "Parque Tecnológico de Álava")
	elif (a.find("spri") != -1) or (a.find("promoción y reconversión") != -1):
		place = Place.objects.get(name_es = "SPRI")
	elif (a.find("enpresa digitala") != -1):
		if (a.find("araba") != -1):
			place = Place.objects.get(name_es = "Araba Enpresa Digitala")
		elif (a.find("zamudio") != -1) or (a.find("bizkaia") != -1):
			place = Place.objects.get(name_es = "Bizkaia Enpresa Digitala")
		elif (a.find("garaia") != -1) or (a.find("arrasate") != -1) or (a.find("mondragón") != -1):
			place = Place.objects.get(name_es = "Garaia Enpresa Digitala")
		elif (a.find("donosti") != -1) or (a.find("miramón") != -1) or (a.find("miramon") != -1) or (a.find("san sebast") != -1):
			place = Place.objects.get(name_es = "Miramón Enpresa Digitala")
	elif  (a.find("polo") != -1) and (a.find("innovación") != -1):
		place = Place.objects.get(name_es = "Polo de Innovación Garaia")
	else:					
		#Look directly at GMaps WS with address
		try:
			resp = urllib2.urlopen(gmaps_url + str(address).replace(" ", "+") +"+españa&sensor=false") 
			xml = resp.read()
			soup = BeautifulStoneSoup(xml)
			if (soup.status.string == 'OK'):
				place = Place(	address = str(soup.formatted_address.string), 
						lat = float(soup.geometry.location.lat.string),
						lng = float(soup.geometry.location.lng.string), 
						prov = get_province(str(soup.findAll("address_component")[2].long_name.string)))
		except:
			pass
		
		if not place:
		#Look at GMaps WS by Postal Code
			cp = pat_cp.findall(a)
			if cp:
				resp = urllib2.urlopen(gmaps_url + str(cp) +"+españa&sensor=false") 
				xml = resp.read()
				soup = BeautifulStoneSoup(xml)
				if (soup.status.string == 'OK'):
					place = Place(	address = str(soup.formatted_address.string), 
							lat = float(soup.geometry.location.lat.string),
							lng = float(soup.geometry.location.lng.string), 
							prov = get_province(str(soup.findAll("address_component")[2].long_name.string)))
	
	#If place isn't set yet, fill it with default "Not Found" place
	if not place:
		place = Place(	address = "Not Found", 
				lat = 0,
				lng = 0, 
				prov = get_province("Otras"))
	
	#Put as names given addresses
	place.name_es = str(address_es)
	place.name_eu = str(address_eu)
	return place

def insertInGCalendar(event):
	cal_client = gdata.calendar.client.CalendarClient(source='InnovAgenda.com')
	cal_client.ClientLogin(gcalendaruser, gcalendarpassword, cal_client.source)

	event_es = gdata.calendar.data.CalendarEventEntry()
	event_es.title = atom.data.Title(text=force_unicode(event.name_es))
	event_es.content = atom.data.Content(text=force_unicode(event.summary_es))
	event_es.where.append(gdata.data.Where(value=force_unicode(event.localization_es)))

	event_eu = gdata.calendar.data.CalendarEventEntry()
	event_eu.title = atom.data.Title(text=force_unicode(event.name_eu))
	event_eu.content = atom.data.Content(text=force_unicode(event.summary_eu))
	event_eu.where.append(gdata.data.Where(value=force_unicode(event.localization_eu)))

	startdat = datetime(event.start_date.year, event.start_date.month, event.start_date.day, event.start_hour.hour, event.start_hour.minute)
	enddat = datetime(event.finish_date.year, event.finish_date.month, event.finish_date.day, event.finish_hour.hour, event.finish_hour.minute)
	start_time = time_tools.strftime('%Y-%m-%dT%H:%M:%S.000Z', time_tools.gmtime(time_tools.mktime(startdat.timetuple())))
	end_time = time_tools.strftime('%Y-%m-%dT%H:%M:%S.000Z', time_tools.gmtime(time_tools.mktime(enddat.timetuple())))
	event_es.when.append(gdata.data.When(start=start_time, end=end_time))
	event_eu.when.append(gdata.data.When(start=start_time, end=end_time))

	ev_es = cal_client.InsertEvent(event_es, insert_uri="http://www.google.com/calendar/feeds/innovagenda.com_d3g76urbacsgv2q8qducmc13og@group.calendar.google.com/private/full")
	ev_eu = cal_client.InsertEvent(event_eu, insert_uri="http://www.google.com/calendar/feeds/innovagenda.com_futd4k5b69sacrfclfrq4jc7bc@group.calendar.google.com/private/full")
	return ev_es.GetHtmlLink().href, ev_eu.GetHtmlLink().href


#-----------------------------------------------------------------------------------------------------------
#f = open("/home/jon/djcode/innovagenda/controllers/" + str(i) + "." + str(j) + "_es" + ".html", "w")
#f.write(soup.prettify())
#f.close()

	
	
#f = open("/home/jon/djcode/innovagenda/controllers/" + str(i) + "." + str(j) + "_eu" + ".html", "w")
#f.write(soup.prettify())
#f.close()

#print str(evid) + '\n' + name_es + '\n' + name_eu + '\n' + str(start_date) + '\n' + str(finish_date) + '\n' + str(start_hour) + '\n' + str(finish_hour) + '\n' + str(duration) + '\n' + str(price) + '\n' + lang_str + '\n\n' + desc_es + '\n\n' + desc_eu + '\n\n' + summary_es + '\n\n' + summary_eu + '\n\n' + str(teacher) + '\n' + url_es + '\n' + url_eu + '\n' + act_str + '\n' + coord_str + '\n' + org_str
#print topic_str
#print "\n\n----------------------------------------------------------\n\n"
