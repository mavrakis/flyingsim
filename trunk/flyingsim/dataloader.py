from google.appengine.ext import bulkload
from google.appengine.api import datastore_types
from google.appengine.ext import search
from google.appengine.ext import db

class AirportLoader(bulkload.Loader):
  def __init__(self):
    # Our 'Person' entity contains a name string and an email
    bulkload.Loader.__init__(self, 'Airport',
                         [('icao_id', str),
                          ('iata_id', str),
                          ('name', str),
                          ('point',lambda x: db.GeoPt(x.split(":")[0],x.split(":")[1])),
                          ('country_code', str),
                          ('country', str),
                          ])

  def HandleEntity(self, entity):
    ent = search.SearchableEntity(entity)
    return ent

if __name__ == '__main__':
  bulkload.main(AirportLoader())