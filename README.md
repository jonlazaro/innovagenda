InnovAgenda
===========

InnovAgenda is a Django-based semantic web app that enables the access to an agenda of events about innovation and technology in Basque Country. It gets data from the web of the Department of Economic Development of Basque Country (Euskadi+Innova), structures it, and publishes it as semantic content through both RDF and schema.org tags.

This project, besides the web visualization itself, provides:

- A script that extracts all information about any event published at http://www.euskadinnova.net/. It looks up the RSS stream provided by Euskadi+Innova from where it gets the URL of the new events; then it scrapps this URL and gets every information about the event, which is structured, geolocated (using Google Maps Geolocation API) and saved it in a relational database.
- A script that automatically mantains a public Google Calendar calendar with the information retrieved by the scrapper.
- An API to access all the data, which returns data in several formats, including RDF (achieved by the extension of Django-Tastypie functionality).

It was developed on 2011 as the Degree Final Project of my BSc in Computer Engineering at University of Deusto (Bilbao).

The complete documentation about InnovAgenda is available in the "docs" folder of this repo (in Spanish).

You can view InnovAgenda working at: http://www.innovagenda.com.
