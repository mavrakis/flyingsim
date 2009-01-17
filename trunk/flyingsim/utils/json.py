#TODO: Factor out
import types
from django.db import models as djangomodels
from django.utils import simplejson as json
from appengine_django.models import BaseModel
from django.core.serializers.json import DateTimeAwareJSONEncoder
from decimal import *

from google.appengine.ext.db import *

class JSONExportable:
    """ In order to allow overwriting JSON export behaviour"""
    def getJSONFields(self):
        ret = {}
        fields = self._entity #_entity keeps track of the fields in the model
        for k in fields:
                try:
                    ret[k] = getattr(self, k)
                except:
                    logging.warning("could not retrieve field %s", k)
        return ret


def json_encode(data):
    """
    The main issues with django's default json serializer is that properties that
    had been added to a object dynamically are being ignored (and it also has 
    problems with some models).
    """

    def _any(data):
        ret = None
        if type(data) is types.ListType:
            ret = _list(data)
        elif type(data) is types.DictType:
            ret = _dict(data)
        elif isinstance(data, JSONExportable):
            #logging.error("Data JSONExportable  %s" , data.getJSONFields())          
               ret =_dict(data.getJSONFields())
        elif isinstance(data, Decimal):
            logging.error("Data Decimal type %s" , data)        
            # json.dumps() cant handle Decimal
            ret = str(data)
        elif isinstance(data, djangomodels.query.QuerySet):        
            # Actually its the same as a list ...
            ret = _list(data)
        elif isinstance(data, djangomodels.Model):          
            ret = _model(data)
        elif isinstance(data, BaseModel):  #appengine_django.models.BaseModel
            logging.error("Data Djangomodel  %s" , data)           
            ret = _modelAppengine(data)            
        elif isinstance(data, GeoPt):
            #logging.error("Data GeoPt  %s" , data)         
            ret = (data.lat,data.lon)
        elif hasattr(data,'__iter__'): #This will match a appengine _QueryIterator
            #logging.error ("hasattr %s", data)
            # Actually its the same as a list ...
            ret = _list(data)          
        else:
            #logging.error("Data Plain  %s" , data)         
            ret = data
        return ret
    
    def _model(data):
        ret = {}
        # If we only have a model, we only want to encode the fields.
        for f in data._meta.fields:
            ret[f.attname] = _any(getattr(data, f.attname))
        # And additionally encode arbitrary properties that had been added.
        fields = dir(data.__class__) + ret.keys()
        add_ons = [k for k in dir(data) if k not in fields]
        for k in add_ons:
            ret[k] = _any(getattr(data, k))
        return ret

    def _modelAppengine(data):
        ret = {}
        fields = data._entity #_entity keeps track of the fields in the model
        for k in fields:
            ret[k] = _any(getattr(data, k))
        return ret
    
    
    def _list(data):
        ret = []
        for v in data:
            ret.append(_any(v))

        #logging.error("Return _list %s" , ret)        
        return ret
    
    def _dict(data):
        ret = {}
        for k,v in data.items():
            ret[k] = _any(v)
        return ret
    
    ret = _any(data)
    #logging.error("Return data %s" , ret)
    return json.dumps(ret, cls=DateTimeAwareJSONEncoder)
