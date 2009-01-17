from django.http import HttpResponse
from django.shortcuts import render_to_response
from google.appengine.ext.db import djangoforms
from google.appengine.ext.db import GeoPt
from google.appengine.api import users
from django.http import HttpResponseRedirect


from django.core import serializers

from google.appengine.ext import bulkload
from flyingsim.dataloader import AirportLoader

from flyingsim.utils.json import json_encode

import datetime
import logging
import models



#Define form class
#class NewFlightForm(djangoforms.ModelForm):
#	class Meta:
#		model=models.Flight
#		exclude=['timeStart','user']


def index(request):
	#return HttpResponse ('<h1>Flyingsim: Coming in 2009</h1>')
	return render_to_response (
		'index2.html',)
	#	{'flights':query.run(),
	#	 'form':NewFlightForm()}

def loadAirport(request):
	bulkload.main(AirportLoader())
	
	return HttpResponse ('<h1>loadAirport</h1>')


def viewFlight(request):
	return render_to_response ('viewFlight.html',)	

def viewAirports(request, queryType="ICAO", query=""):
	logging.error("getFlightData %s %s" ,queryType,query)
	
	if queryType.upper() == "IATA":
	   query = models.Airport.gql("Where iata_id=:1 ORDER BY iata_id DESC", query.upper())
	else:
		query = models.Airport.gql("Where icao_id=:1 ORDER BY icao_id DESC", query.upper())
	
	qAirports = query.run()
	airports=[]
	for qAirport in qAirports:
		airports.append(qAirport)
	
	#assert(False)
	return render_to_response('viewAirport.html',{'airports':airports,'title':'Airports of the world'})

def doLogin(request):
	flight =models.Flight.gql("ORDER by sessionId DESC").get()
	if flight==None:
		sessionId=1
	else:
		sessionId=flight.sessionId+1
	
		
	data = json_encode({'sessionId':sessionId})
	
	return HttpResponse(data)

def doStartFlight(request):
	queryDict = request.GET
	sessionId=queryDict.get('sessionId')
	airportStart=queryDict.get('airportStart')
	airportEnd=queryDict.get('airportEnd')
	
	flight = models.Flight.findFlight(airportStart,airportEnd)
	flight.timeStart=datetime.datetime.now()
	flight.timestampUpdatedServer=datetime.datetime.now()
	flight.timestampPolledClient=datetime.datetime.now()
	flight.sessionId=int(sessionId)
	flight.put()
	
	data = json_encode(flight)
	logging.error("doStartFlight %s" , data) 	
	return HttpResponse (data)

def getFlightData(request):
	queryDict = request.GET
	sessionId=queryDict.get('sessionId')

	#flight= models.Flight.get_by_id(43)
	#assert(False)
	flightQuery= models.Flight.gql("Where sessionId=:1", sessionId)
	flight=flightQuery.get()
	
	flight.updateFlight()
	flight.put()
	
	data = json_encode(flight)
	logging.error("getFlightData %s" , data) 
	return HttpResponse (data)
	
def getFlightDataOther(request):
	return HttpResponse ('<h1>api:getFlightDataOther</h1>')

def getFlightRoute(request):
	queryDict = request.GET
	sessionId=queryDict.get('sessionId')
	airportStart=queryDict.get('airportStart')
	airportEnd=queryDict.get('airportEnd')	
	
	flight = models.Flight.findFlight(airportStart,airportEnd)
	flight.put()
	data=json_encode(flight)
	return HttpResponse (data)
	
def getPossibleAirportStart(request):
	query = models.Airport.gql("ORDER BY name DESC");
	airports=query.run()
	#airports=models.Airport.objects.all()
	#data = simplejson.dumps(flights.objects.all)
	data=json_encode(airports)

	return HttpResponse (data)

def getPossibleAirportEnd(request):
	queryDict = request.GET
	airportStart=queryDict.get('airportStart')
	airports=models.Airport.findAvailableAirportsFrom(airportStart)
	data=json_encode(airports)
	return HttpResponse (data)


def testData(request):
	models.Airport(name="Stavanger",icao_id="SVG",point=GeoPt(70.10,71.20)).put()
	models.Airport(name="Oslo",icao_id="OSL",point=GeoPt(40.10,41.20)).put()
	return HttpResponse ('<h1>Test data added</h1>')







def post(request):
	form = NewFlightForm(request.POST)
	if not form.is_valid():
			return render_to_response (
				'index.html',
				{'form':form})
	
	flight=form.save(commit=False)
	flight.user=users.get_current_user()
	flight.put()
	logging.error("Put result %s", str(flight.is_saved()))
	return HttpResponseRedirect('/')
	
	 
#return HttpResponse ('Hello flyingsim')


