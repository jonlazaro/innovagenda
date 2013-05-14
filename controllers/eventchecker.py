# encoding: utf-8

from website.models import Event
from datetime import date, time, datetime

def check_if_finished():
	print "...Looking for FINISHED events...\n"
	#Today finishing events
	for ev in (Event.objects.filter(finished=False, finish_date=datetime.now().date())):
		#Check if it's already finished
		if (ev.finish_hour <= datetime.datetime.now().time()):
			ev.finished = True
			ev.save()
			print "EVENT " + str(ev.internal_id) + " has already FINSISHED"
	print "...Look up finished..."
