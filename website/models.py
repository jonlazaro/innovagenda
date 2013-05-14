# encoding: utf-8
from django.db import models
from transmeta import TransMeta

# Create your models here.
class ActivityType(models.Model): #Autodiscover + Curso, Jornada, Barnetegi, Taller, Conferencia, Exposición, Congreso, Feria, Reunion
	__metaclass__ = TransMeta

	name = models.CharField(blank=False, max_length=30)
	
	class Meta:
		translate = ('name', )

	def __unicode__(self):
		return self.name
	
class Topic(models.Model): #Innovación Tecnológica, Innovación Social, Transformación Empresarial, Enpresa Digitala
	__metaclass__ = TransMeta

	name = models.CharField(blank=False, max_length=30)
	
	class Meta:
		translate = ('name', )

	def __unicode__(self):
		return self.name
		
class Agency(models.Model): #Autodiscover
	name = models.CharField(blank=False, max_length=200)
	
	def __unicode__(self):
		return self.name

class Province(models.Model): #Otros + Bizkaia, Gipuzkoa, Araba
	__metaclass__ = TransMeta
	
	name = models.CharField(blank=False, max_length=30)
	
	def __unicode__(self):
		return self.name

	class Meta:
		translate = ('name', )

class Language(models.Model): #Otros + Euskera, Castellano, Ingles
	__metaclass__ = TransMeta
	
	name = models.CharField(blank=False, max_length=30)
	
	def __unicode__(self):
		return self.name

	class Meta:
		translate = ('name', )
		
class Place(models.Model):
	__metaclass__ = TransMeta
	
	name = models.CharField(blank=False, max_length=50)
	address = models.CharField(max_length=300)
	lat = models.FloatField()
	lng = models.FloatField()

	prov = models.ForeignKey(Province)

	class Meta:
		translate = ('name', )
	
	def __unicode__(self):
		return self.name

class Event(models.Model):
	__metaclass__ = TransMeta

	event_id = models.IntegerField()
	name = models.CharField(max_length=150)
	inserted_date = models.DateTimeField(auto_now_add=True)
	start_date = models.DateField()
	finish_date = models.DateField(blank=True, null=True)
	start_hour = models.TimeField(blank=True, null=True)
	finish_hour = models.TimeField(blank=True, null=True)
	duration = models.IntegerField(blank=True, null=True)
	price = models.FloatField(blank=True, null=True)
	description = models.CharField(max_length=10000)
	summary = models.CharField(max_length=3000)
	teacher = models.CharField(max_length=50, blank=True, null=True)
		
	url = models.CharField(max_length=300)
	gcalendar_url = models.CharField(max_length=300)
	finished = models.BooleanField(default=False)

	localization = models.CharField(max_length=300)
	address = models.CharField(max_length=300)
	lat = models.FloatField()
	lng = models.FloatField()

	prov = models.ForeignKey(Province)
	course_lang = models.ForeignKey(Language)
	activity_type = models.ForeignKey(ActivityType)
	topic = models.ForeignKey(Topic)
	coordinator = models.ForeignKey(Agency, related_name="event_coordinator")
	organizator = models.ForeignKey(Agency, related_name="event_organizator")
		
	def set_foreign_data(self, act_type, topic, coord, org, lang):
		#Activity Type
		act_type, created = ActivityType.objects.get_or_create(name_es = act_type)
		if created:
			act_type.save()
		self.activity_type = act_type

		#Topic
		try:
			self.topic = Topic.objects.get(name_es = topic)
		except Topic.DoesNotExist:
			self.topic = Topic.objects.get(name_es = 'Otros')
	
		#Coordinator
		coord, created = Agency.objects.get_or_create(name=coord)
		if created:
			coord.save()
		self.coordinator = coord
        
		#Organizator
		org, created = Agency.objects.get_or_create(name=org)
		if created:
			org.save()
		self.organizator = org

		#Course Language
		if (lang in ['Español', 'Castellano']):
			self.course_lang = Language.objects.get(name_es = 'Castellano')
		elif (lang in ['Euskera', 'Vasco']):
			self.course_lang = Language.objects.get(name_es = 'Euskera')
		elif (lang in ['Inglés', 'Ingles', 'English']):
			self.course_lang = Language.objects.get(name_es = 'Inglés')
		else:
			self.course_lang = Language.objects.get(name_es = 'Otros')

		
	class Meta:
		translate = ('name', 'description', 'summary', 'url', 'localization', 'gcalendar_url', )    
		
	def __unicode__(self):
		return u'%s %s' % (str(self.start_date), self.name)
