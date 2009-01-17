class GeoUtils:
#From http://groups-beta.google.com/group/Google-Maps-API/browse_thread/thread/20fadd10c5557c50/fdd0fc490229dea3?q=math.cos&rnum=2#fdd0fc490229dea3
    def distanceBetween(geoPtA, geoPtB):        
        aLatRad = math.radians(geoPtA.lat)
        aLonRad = math.radians(geoPtA.lon)
        bLatRad = math.radians(geoPtB.lat)
        bLonRad = math.radians(geoPtB.lon)
        
        dist = math.sin(aLatRad) * math.sin(bLatRad) + math.cos(aLatRad) * math.cos(bLatRad) * math.cos(aLonRad - bLonRad);
    
        dist = math.acos(dist)
        dist = math.degrees(dist)
        miles = dist * 60 * 1.1515
        meters = miles * 1000 * 1.609344
        return meters
    distanceBetween=staticmethod(distanceBetween)
    
    #from http://svn.geotracing.codehaus.org/browse/geotracing/base/trunk/server/webapp/gt/lib/GMap.js?r=201
    def headingRadians(geoPtFrom, getPtTo):
        fromLatRad = math.radians(geoPtFrom.lat)
        fromLonRad = math.radians(geoPtFrom.lon)
        toLatRad = math.radians(getPtTo.lat)
        toLonRad = math.radians(getPtTo.lon)
    
        v1 = math.sin(fromLonRad - toLonRad) * math.cos(toLatRad)
        v2 = math.cos(fromLatRad) * math.sin(toLatRad) - math.sin(fromLatRad) * math.cos(toLatRad) * math.cos(fromLonRad - toLonRad)
        #rounding error protection
        if abs(v1) < 1e-15:
            v1 = 0.0;
        if abs(v2) < 1e-15:
            v2 = 0.0;
        return math.atan2(v1, v2)
    headingRadians=staticmethod(headingRadians)
    
    def newPointInHeadingAndDistance(geoPtFrom, headingRadians, meters):
        lon = math.radians(geoPtFrom.lon)
        lat = math.radians(geoPtFrom.lat)
        
        RADIAN = 180 / math.pi
    
        f = 1 / 298.257
        e = 0.08181922
    
        EARTH_RADIUS_EQUATOR = 6378140.0
        R = EARTH_RADIUS_EQUATOR * (1 - e * e) / math.pow((1 - e * e * math.pow(math.sin(lat), 2)), 1.5)
    
        psi = meters / R
        phi = math.pi / 2 - lat
        arccos = math.cos(psi) * math.cos(phi) + math.sin(psi) * math.sin(phi) * math.cos(headingRadians)
        newLat = (math.pi / 2 - math.acos(arccos)) * RADIAN
        arcsin = math.sin(headingRadians) * math.sin(psi) / math.sin(phi)
        newLng = (lon - math.asin(arcsin)) * RADIAN
    
        #echo "***long=$long asin(arcsin)=".asin($arcsin) . " radian=$RADIAN <br>";
        #echo "PSI=$psi PHI=$phi arccos=$arccos arcsin=$arcsin newLat=$newLat newLng=$newLng";
    
        newPoint = GeoPt(newLat, newLng)
        return newPoint
    newPointInHeadingAndDistance=staticmethod(newPointInHeadingAndDistance)
