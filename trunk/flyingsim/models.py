from appengine_django.models import BaseModel
from google.appengine.ext import db
from google.appengine.ext.db import GeoPt
from google.appengine.ext.search import SearchableModel

#Python imports
import math
import datetime, time
import logging

#Local imports
from flyingsim.utils.geoutils import GeoUtils
from flyingsim.utils.json import JSONExportable
from flyingsim.utils.json import json_encode

# Create your models here.

class Waypoint(BaseModel, JSONExportable):
	"""" Representing a waypoint in a flight plan"""
	wpt_id = db.StringProperty(required=True)
	point = db.GeoPtProperty(required=True)

class Country(SearchableModel, JSONExportable):
	name=db.StringProperty(required=True)
	code=db.StringProperty()
	region=db.StringProperty()
	
	
class Airport(SearchableModel, JSONExportable):
	""" Representing an airport of the world"""
	sequence_nr=db.IntegerProperty(required=True)
	icao_id = db.StringProperty(required=True)
	name = db.StringProperty(required=True)
	iata_id = db.StringProperty()
	#country=db.StringProperty()
	country=db.ReferenceProperty(Country)
	point = db.GeoPtProperty(required=True)
	def getJSONFields(self):
		ret = super(Airport, self).getJSONFields()
		ret['latitude'] = self.point.lat
		ret['longitude'] = self.point.lon
		ret['icaoID'] = self.icao_id
		ret['country'] = self.country
		ret['iata_id'] = self.iata_id
		return ret
	
	def findAvailableAirportsFrom(airportFromICAO):
		query = Airport.gql("Where icao_id!=:1 ORDER BY icao_id DESC", airportFromICAO)
		airports = query.run()
		return airports
	findAvailableAirportsFrom = staticmethod(findAvailableAirportsFrom)
	
	def closestToPointExact(airportA, airportB, point):
		distSumA =GeoUtils.distanceBetween(airportA.point,point)
		airportA.distanceTo=distSumA
		distSumB= GeoUtils.distanceBetween(airportB.point,point)
		airportB.distanceTo=distSumB
		
		if distSumA>distSumB:
			return 1
		elif distSumA==distSumB:
			return 0
		else:
			return -1
	closestToPointExact=staticmethod(closestToPointExact)

	def closestToPointSimple(airportA, airportB, point):
		distLatA = math.fabs(max(airportA.point.lat, point.lat) - min(airportA.point.lat, point.lat))
		distLonA = math.fabs(max(airportA.point.lon, point.lon) - min(airportA.point.lon, point.lon))
		distSumA= distLatA+distLonA
		
		distLatB = math.fabs(max(airportB.point.lat, point.lat) - min(airportB.point.lat, point.lat))
		distLonB = math.fabs(max(airportB.point.lon, point.lon) - min(airportB.point.lon, point.lon))
		distSumB= distLatB+distLonB
		
		if distSumA>distSumB:
			return 1
		elif distSumA==distSumB:
			return 0
		else:
			return -1
	closestToPointSimple=staticmethod(closestToPointSimple)
				
	
class Airway(BaseModel, JSONExportable):
	name = db.StringProperty()	
	pointStart = db.GeoPtProperty(required=True)
	pointEnd = db.GeoPtProperty(required=True)

class Plane(BaseModel, JSONExportable):
	name = db.StringProperty(required=True)
	capacity = db.IntegerProperty()
	speed = db.FloatProperty()
	range = db.FloatProperty()
	icon = db.TextProperty()

class FlightState(BaseModel, JSONExportable):
	name = db.StringProperty(required=True)
	isStartState = db.BooleanProperty()
	description = db.TextProperty(required=True)


class Flight(BaseModel, JSONExportable):
	#General flight information
	sessionId = db.IntegerProperty()
	description = db.StringProperty()
	airportFrom = db.ReferenceProperty(Airport, collection_name="flight_airport_from_set")
	airportTo = db.ReferenceProperty(Airport, collection_name="flight_airport_to_set")
	plane = db.ReferenceProperty(Plane)
	timeStart = db.DateTimeProperty(auto_now_add=True)
	completed = db.BooleanProperty(default=False)
	timeEnd = db.DateTimeProperty()
	user = db.UserProperty()
	#Information used during flight
	airways = None#db.ListProperty(Airway,default=None)
	waypoints = None#db.ListProperty(GeoPt,default=None)
	currentPoint = db.GeoPtProperty()
	headingRadians = db.FloatProperty(default=0.0)
	speed = db.FloatProperty(default=3000.0)
	state = db.ReferenceProperty(FlightState)
	targetId = db.TextProperty()
	targetPoint = db.GeoPtProperty()
	timestampUpdatedServer = db.DateTimeProperty()
	timestampPolledClient = db.DateTimeProperty()

	def getJSONFields(self):
		ret = super(Flight, self).getJSONFields()
		ret['currentLat'] = self.currentPoint.lat
		ret['currentLng'] = self.currentPoint.lon
		waypoints = [{'latitude':40.0, 'longitude':50.0}]
		ret['waypoints'] = waypoints
		return ret	
	
	def findFlight(airportFromICAO, airportToICAO):
			retFlight = Flight()
			airportFrom = Airport.gql("Where icao_id=:1", airportFromICAO).get()
			airportTo = Airport.gql("Where icao_id=:1", airportToICAO).get()
			retFlight.airportFrom = airportFrom
			retFlight.airportTo = airportTo
			retFlight.currentPoint = airportFrom.point
			
			#TODO: Add waypoints and other information
			#waypoints=[]
			#waypoints.append(GeoPt(50,60))
			#retFlight.waypoints=waypoints
			
			retFlight.targetId = airportToICAO
			retFlight.targetPoint = airportTo.point

			return retFlight
	findFlight = staticmethod(findFlight)
	
	  
	def getWaypointAfter(self, waypointId):
		for k, waypoint in self.waypoints:
			if waypoint.wpt_id == waypointId:
				if k == len(self.waypoints):
					#last waypoint
					return None
				else:
					return waypoint
		#found no waypoint
		return None
	


	def updateFlight(self):
		timestampLastUpdated = self.timestampUpdatedServer
		timestampNow = datetime.datetime.now()
		
		
		timeDeltaSinceLastUpdate = timestampNow - timestampLastUpdated;
		timeSinceLastUpdate = timeDeltaSinceLastUpdate.seconds + timeDeltaSinceLastUpdate.microseconds / 1000000.0
		logging.debug ("timeSinceLastUpdate %s", timeSinceLastUpdate)
		
		speedMS = self.speed
		
		pointTarget = self.targetPoint
		pointPlane = self.currentPoint
		
		count = 0;
		
		#While loop which runs if we're going to pass the current (potentially many) waypoint/target
		while GeoUtils.distanceBetween(pointTarget, pointPlane) < timeSinceLastUpdate * speedMS:
			count = count + 1
			if count > 20:
				logging.error ("unplanned infinite loop..")
				#echo "timeSinceLastUpdate=$timeSinceLastUpdate New point location=".$pointPlane->toString(). " New target ".$pointTarget->toString() . "Distance=".$pointTarget->distanceFrom($pointPlane);
				return
			
			#substract time to use to current target
			timeSinceLastUpdate = timeSinceLastUpdate - (GeoUtils.distanceBetween(pointTarget, pointPlane) / speedMS)
			
			#move plane to target
			pointPlane = planeTarget
			
			#TODO: update target completion
			waypointNext = self.getWaypointAfter(self.targetId)
			if waypointNext == None:
				logging.error ("No next waypoint. TODOHANDLE")
				return
			else :
				pointTarget = waypointNext
				self.targetPoint = waypointNext
				self.targetId = waypointNext.wpt_id
				
			#echo "timeSinceLastUpdate=$timeSinceLastUpdate New point location=".$pointPlane->toString(). " New target ".$pointTarget->toString() . "Distance=".$pointTarget->distanceFrom($pointPlane);
			#TODO: Check if flight complete/state changed
		
		
		#end of while loop means we will not pass current waypoint/target
		
		headingRad = GeoUtils.headingRadians(pointPlane, pointTarget)
		metersTravelled = timeSinceLastUpdate * speedMS;
		logging.error ("headingRad=%s meters=%s", headingRad, metersTravelled)
		pointPlaneNew = GeoUtils.newPointInHeadingAndDistance(pointPlane, headingRad, metersTravelled)
		#Update FlightData
		self.currentPoint = pointPlaneNew
		
		logging.error ("old_loc=%s new_loc=%s distance=%s", pointPlane, pointPlaneNew, distanceBetween(pointPlane, pointPlaneNew))
		
		self.timestampUpdatedServer = timestampNow
		self.headingRadians = GeoUtils.headingRadians(pointPlaneNew, pointTarget)
		#echo "New location " . $pointPlane->toString();
		
		self.put()

	