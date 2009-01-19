from django.http import HttpResponse
from django.shortcuts import render_to_response
from google.appengine.ext.db import djangoforms
from google.appengine.ext.db import GeoPt
from google.appengine.api import users
from django.http import HttpResponseRedirect
from google.appengine.api import memcache

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
	countries=getAllCountries()

	return render_to_response (
		'viewStartPage.html',{'countries':countries})
	#	{'flights':query.run(),
	#	 'form':NewFlightForm()}

def getAllCountries():
	countries = memcache.get("countries")
	if countries is not None:
		#logging.error("Getting countries from memcache")
		return countries
	else:
		countryQuery = models.Country.all().order('name')
		countries=[]
		for qCountry in countryQuery:
			countries.append(qCountry)
		logging.error("Adding countries to memcache")
		memcache.add("countries", countries)
        return countries

def getAllAirports():
	#TODO: Memcache
	airports=[]
	airportQuery1 = models.Airport.all().order('sequence_nr').fetch(1000)
	for qAairport in airportQuery1:
		airports.append(qAairport)
	
	#airportQuery2 = models.Airport.all().order('sequence_nr').filter('sequence_nr >= ', 1000)
	#for qAairport in airportQuery2:
	#	airports.append(qAairport)
			
	#airportQuery3 = models.Airport.all().order('sequence_nr').filter('sequence_nr >= ', 2000)
	#for qAairport in airportQuery3:
	#	airports.append(qAairport)
			
	#airportQuery4 = models.Airport.all().order('sequence_nr').filter('sequence_nr >= ', 3000)
	#for qAairport in airportQuery4:
	#	airports.append(qAairport)	

	logging.error('Got %s airports ', len(airports) )
	return airports


def loadAirport(request):
	bulkload.main(AirportLoader())
	
	return HttpResponse ('<h1>loadAirport</h1>')

def delAirport(request):
	airportQuery1 = models.Airport.all().fetch(200)
	
	counter = 0
	for qAairport in airportQuery1:
		qAairport.delete()
		counter = counter +1 
	
#	airportQuery2 = models.Airport.all().order('sequence_nr').filter('sequence_nr >= ', 1000)
#	for qAairport in airportQuery2:
#		airports.append(qAairport)
			
#	airportQuery3 = models.Airport.all().order('sequence_nr').filter('sequence_nr >= ', 2000)
#	for qAairport in airportQuery3:
#		airports.append(qAairport)
			
#	airportQuery4 = models.Airport.all().order('sequence_nr').filter('sequence_nr >= ', 3000)

#	for qAairport in airportQuery4:
#		airports.append(qAairport)	
	
#	bulkload.main(AirportLoader())
	
	return HttpResponse ('<h1>Deleted airports ' + str(counter) + '</h1>')



def viewFlight(request):
	return render_to_response ('viewFlight.html',)	

def searchAirports(request):
	""" Method used for redirecting POST queries to REST based GET URLS """
	queryDict = request.POST
	searchBy=queryDict.get('searchBy','icao')
	if searchBy.upper()=="CLOSETO":
		lat=queryDict.get('lat')
		lon=queryDict.get('lon')
		query="("+str(lat)+","+str(lon)+")"
	else:
		query=queryDict.get('query','empty')
	
	logging.debug("searchAirports %s %s" ,searchBy,query)
	
	return HttpResponseRedirect('/airports/'+searchBy+'/'+query+'/')
		

def viewAirports(request, queryType="", query=""):
	logging.error("viewAirports %s %s" ,queryType,query)
	
	countries=getAllCountries()
	logging.error("after getting countries")
	searchDone='Airports with ' +queryType+ ' '+query
	
	if queryType.upper() == "IATA":
		queryStatement = models.Airport.gql("Where iata_id=:1 ORDER BY iata_id DESC", query.upper())
	elif queryType.upper() == "ICAO":
		queryStatement = models.Airport.gql("Where icao_id=:1 ORDER BY icao_id DESC", query.upper())
	elif queryType.upper() == "NAME":
		queryStatement = models.Airport.all().search(query)
	elif queryType.upper() == "COUNTRY":
		#Too slow to use country reference attribute..
		#case must match when using filter
		#countryList = models.Country.all().filter('name = ', query).fetch(limit=1)
		
		queryStatement = models.Airport.gql("Where country=:1", query)
		
		#countryList = models.Country.all().search(query)	
		#if countryList.count()!=0:
		#	queryStatement = models.Airport.gql("Where country=:1", countryList[0].key())
		#else:
		#	logging.info('viewAirports: Could not find country %s . Search fails ' , query)
		#	return viewAirportsFailed(request,countries,queryType,query,searchDone,"Could not find country "+query)
	elif queryType.upper() == "CLOSETO":
		searchDone='Airports which are close to the geolocation' +query
		return viewAirportsCloseTo2(request,countries,queryType,query,searchDone)
	else:
		return viewAirportsFailed(request,countries,queryType,query,"No search parameters","Please select the search tab above and perform a search")
	
	logging.error("Before query run")
	qAirports = queryStatement.run()
	logging.error("after query run")
	airports=[]
	for qAirport in qAirports:
		airports.append(qAirport)
	
	logging.error("after loop")
	
	if not airports:
		return viewAirportsFailed(request,countries,queryType,query,searchDone,"No airports found for search by " + queryType + " with value " +query)
	
	return render_to_response('viewAirport.html',
							  {'airports':airports,'countries':countries,'searchDone':searchDone, 'title':'Flyingsim.com: ' + searchDone})

def viewAirportsFailed(request,countries,queryType, query, searchDone, reason):
	return render_to_response('viewAirport.html',
							  {'airports':[],'countries':countries,'searchDone':searchDone,'reason':reason,
							    'title':'Flyingsim.com: ' + reason})

#def viewAirportsCloseTo(request,countries,queryType, query, searchDone,nrAirports=10):
#	""" This method gets all airports, sort through them and filters out far away..Too slow """
#	
#	try:
#		location=query.replace("(","").replace(")","")
#		firstToken = location.split(",")[0]
#		lastToken=location.split(",")[1]
#		#logging.error("Tokens %s %s", firstToken,lastToken )
#		point=GeoPt(float(firstToken),float(lastToken))
#	except:
#		logging.error("Failed to convert %s", location )
#		return viewAirportsFailed(request,countries,queryType,query,searchDone,"Failed to convert location" +query+" to valid point")	
#	
#	airports=getAllAirports()
#	
#	airports.sort(cmp=lambda x,y: models.Airport.closestToPointSimple(x,y,point))
#	closeAirports=airports[0:50]
#	closeAirports.sort(cmp=lambda x,y: models.Airport.closestToPointExact(x,y,point))
#	closeAirports=closeAirports[0:nrAirports]
#	
#	return render_to_response('viewAirport.html',
#							  {'pointCloseTo':point,'airports':closeAirports,'countries':countries,'searchDone':searchDone,
#							    'title':'Flyingsim.com: ' + searchDone})

def viewAirportsCloseTo2(request,countries,queryType, query, searchDone,nrAirports=10):
	try:
		location=query.replace("(","").replace(")","")
		firstToken = location.split(",")[0]
		lastToken=location.split(",")[1]
		#logging.error("Tokens %s %s", firstToken,lastToken )
		point=GeoPt(float(firstToken),float(lastToken))
	except:
		logging.error("Failed to convert %s", location )
		return viewAirportsFailed(request,countries,queryType,query,searchDone,"Failed to convert location" +query+" to valid point")	
	
	pointLat= int(point.lat)
	pointLon= int(point.lon)
	maxLat=int(pointLat+5)
	minLat=int(pointLat-5)
	maxLon=int(pointLon+5)
	minLon=int(pointLon-5)
	logging.debug("First searcg WHERE pointLon < %s AND pointLon > %s",maxLon,minLon)

	airportQuery1 = models.Airport.gql("Where pointLat < :1 AND pointLat > :2 ",maxLat,minLat).fetch(1000)
	
	airports=[]
	for qAirport in airportQuery1:
		if qAirport.pointLon < maxLon and qAirport.pointLon > minLon:
		  airports.append(qAirport)
	
	logging.error("After toArray and Lat filtering length=%s", len(airports))
	
	airports.sort(cmp=lambda x,y: models.Airport.closestToPointSimple(x,y,pointLat,pointLon))
	closeAirports=airports[0:nrAirports]
	closeAirports.sort(cmp=lambda x,y: models.Airport.closestToPointExact(x,y,point))
	closeAirports=closeAirports[0:nrAirports]
	
	return render_to_response('viewAirport.html',
							  {'pointCloseTo':point,'airports':closeAirports,'countries':countries,'searchDone':searchDone,
							    'title':'Flyingsim.com: ' + searchDone})
	
	


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






