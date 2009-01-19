from google.appengine.ext import bulkload
from google.appengine.api import datastore_types
from google.appengine.ext import search
from google.appengine.ext import db
from google.appengine.api import datastore_entities
from google.appengine.api import datastore

from google.appengine.api.datastore_errors import NeedIndexError 

import logging
import models

class AirportLoader(bulkload.Loader):
  def __init__(self):
    # Our 'Person' entity contains a name string and an email
    logging.error("init self")
    self.sequence_nr=1
    bTry=True
    while bTry:
        try:
            lastAirport = models.Airport.all().order('-sequence_nr').fetch(1)
            bTry=False
            if lastAirport:
                self.sequence_nr=lastAirport[0].sequence_nr
            
        except OSError:
            logging.error("Got OS error")
        except NeedIndexError:
            bTry=False
                

    
    
    bulkload.Loader.__init__(self, 'Airport',
                         [('icao_id', str),
                          ('iata_id', str),
                          ('name', str),
                          ('point',lambda x: db.GeoPt(x.split(":")[0],x.split(":")[1])),
                          ('country_code', str),
                          ('country', str),
                          ])

  def HandleEntity(self, entity):
    logging.error ("HandleEntity %s " ,entity)
        
    #airport = models.Airport(name=entity['name'],icao_id=entity['icao_id'],iata_id=entity['iata_id'],point=entity['point'])
    #models.Airport(name="Stavanger",icao_id="SVG",point=GeoPt(70.10,71.20))
    #airport.put()
    #event.update(entity)
    countryStr=entity['country']
    if countryStr:
        bTry=True
        while bTry:
            try:
                countryObj = models.Country.gql("Where name=:1",countryStr).get()
                bTry=False
            except OSError:
                logging.error("Got OS error")
        

        if not countryObj:
            countryObj=models.Country(name=countryStr, code=entity['country_code'])
            #logging.error ("Storing country %s " ,countryStr) 
            bTry=True
            while bTry:
                try:
                    countryObj.put()
                    bTry=False
                except OSError:
                    logging.error("Got OS error")
           

        #logging.error ("country %s " ,countryObj[0]) 
        entity['country']=countryObj.key()
    
    
    del entity['country_code']    
    entity = search.SearchableEntity(entity)  
    #required in order to retrieve more than 1000 elements
    entity['sequence_nr']=self.sequence_nr
    self.sequence_nr= self.sequence_nr +1
    
    logging.error ("entity right before return %s " ,entity) 
    return entity


  #def HandleEntity(self, entity): 
  #  event = datastore_entities.Event(entity.title) 
  #  event.update(entity) 
  #  creator = event['creator'] 
  #  if creator: 
  #    contact = datastore.Query('Contact', {'title': creator}).Get(1) 
  #    if not contact: 
  #      contact = [datastore_entities.Contact(creator)] 
  #      datastore.Put(contact[0]) 
  #    event['author'] = contact[0].key() 
  #  return event 

if __name__ == '__main__':
  bulkload.main(AirportLoader())