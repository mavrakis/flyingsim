# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf.urls.defaults import *

urlpatterns = patterns(
	#'',
	'flyingsim.views',
	(r'^$', 'index'),
#	(r'^loadAirport/$', 'loadAirport'),	
#	(r'^delAirport/$', 'delAirport'),		
	(r'^airports/$', 'viewAirports'),
	(r'^airports/(?P<queryType>\w+)/(?P<query>.+)/$', 'viewAirports'),
	(r'^airports/search/$', 'searchAirports'),	
	(r'^flight/$', 'viewFlight'),
	(r'^prototype/3/api/doLogin/$', 'doLogin'),
	(r'^prototype/3/api/doStartFlight/$', 'doStartFlight'),	
	(r'^prototype/3/api/getFlightData/$', 'getFlightData'),	
	(r'^prototype/3/api/getFlightDataOther/$', 'getFlightDataOther'),
	(r'^prototype/3/api/getFlightRoute/$', 'getFlightRoute'),	
	(r'^prototype/3/api/getPossibleAirportEnd/$', 'getPossibleAirportEnd'),	
	(r'^prototype/3/api/getPossibleAirportStart/$', 'getPossibleAirportStart'),	
	(r'^prototype/3/api/testData/$', 'testData'),
	
#	(r'^admin/', include('django.contrib.admin.urls')),
# Example:
# (r'^foo/', include('foo.urls')),
#     Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)
