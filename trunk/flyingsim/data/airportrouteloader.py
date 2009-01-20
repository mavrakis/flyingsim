from google.appengine.ext import bulkload
from google.appengine.api import datastore_types
from google.appengine.ext import search
from google.appengine.ext import db
from google.appengine.api import datastore_entities
from google.appengine.api import datastore

from google.appengine.api.datastore_errors import NeedIndexError 

import logging
from flyingsim import models

class AirportRouteLoader(bulkload.Loader):
  def __init__(self):
    # Our 'Person' entity contains a name string and an email
    logging.error("init self")
    self.sequence_nr=1
    bTry=True
    while bTry:
        try:
            last = models.AirportRoute.all().order('-sequence_nr').fetch(1)
            bTry=False
            if last:
                self.sequence_nr=last[0].sequence_nr
            
        except OSError:
            logging.error("Got OS error")
        except NeedIndexError:
            bTry=False
                

    
    
    bulkload.Loader.__init__(self, 'AirportRoute',
                         [('icao_from', str),
                          ('to_icao_id',str),
                          ])

  def HandleEntity(self, entity):
    logging.error ("HandleEntity %s " ,entity)
        
    to_icao_id=entity['to_icao_id']
    if to_icao_id:
        bTry=True
        while bTry:
            try:
                airportObj = models.Airport.gql("Where icao_id=:1",to_icao_id).get()
                bTry=False
            except OSError:
                logging.error("Got OS error")

        #Add the key
        entity['airport_to']=airportObj.key()
    
    del entity['to_icao_id']
    entity['sequence_nr']=self.sequence_nr
    self.sequence_nr= self.sequence_nr +1
    
    logging.error ("entity right before return %s " ,entity) 
    return entity


 
if __name__ == '__main__':
  bulkload.main(AirportRouteLoader())