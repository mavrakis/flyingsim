# coding=iso-8859-1

import string

#Map between ICAO and IATA if possible
class ICAOIATAMapper():
    mapping = {}
    bIsInit=False
    
    def init(self):
        print "In init mapper"
        file = open('C:\\DEV\\work\\data.x-plane.com\\work\\wiki_icao.html', 'r')
        for line in file:
            if line.startswith ("<li><b>"):
                self.processLine(line)
        bIsInit=True
    
    def processLine(self,line):
        strLine = line[7:22]
        strLine=strLine.replace("</b>","")
        if strLine.find("(")!=-1:
            tokens=strLine.split()
            icao = tokens[0].strip()
            iata = tokens[1].strip()
            iata=iata [1:-1]
            #print icao + "=" + iata
            self.mapping[icao]=iata
            
    def getIATAFromICAO(self,icao):
        if self.bIsInit==False:
            self.init()
            self.bIsInit=True
        if icao in self.mapping:
            return self.mapping[icao]
        else:
            return None

class APTAirport():
    def process(self,mapper):
        arAirportTokens =self.strAirportLine.split()
        self.icao_id= arAirportTokens[4]
        
        self.iata_id=mapper.getIATAFromICAO(self.icao_id)
        
        self.country_code=self.icao_id[0:2]
        self.country=self.country_from_country_code(self.country_code)
        if self.country!=None:
            self.country=self.country.replace('"', '\\"').replace("'", "\\'")
        self.name=""
        i=5
        while i < len(arAirportTokens):
            self.name+=arAirportTokens [i]+" "
            i=i+1
        self.name=self.name.strip()
        self.name=self.name.replace('"', '\\"').replace("'", "\\'")
        self.name=string.capwords(self.name)
        
        self.valid=True
        if self.name.find("[x]")!= -1:
            self.valid=False
        
        if self.country==None:
            self.valid=False
        
        if self.iata_id==None:
            self.valid=False
        
            
        #self.name=self.strAirportLine.
        arRunwayTokens =self.strRunwayLine.split()
        self.strPoint=arRunwayTokens[9] + ":" + arRunwayTokens[10]
        
        
    def toCSV(self):
        return "\"" + self.icao_id + "\",\""+str(self.iata_id)+"\",\""+self.name+"\",\"" + self.strPoint + "\",\"" +self.country_code+"\",\""+str(self.country)+"\""
        
    def country_from_country_code(self,strCode):
        dictCountry={"AG":"Solomon Islands",
        "AN":"Nauru",
        "AY":"Papua New Guinea",
        "BG":"Greenland",
        "BI":"Iceland",
        "BK":"Kosovo",
        "C":"Canada",
        "DA":"Algeria",
        "DB":"Benin",
        "DF":"Burkina Faso",
        "DG":"Ghana",
        "DI":"Côte d'Ivoire",
        "DN":"Nigeria",
        "DR":"Niger",
        "DT":"Tunisia",
        "DX":"Togolese Republic",
        "EB":"Belgium",
        "ED":"Germany",
        "EE":"Estonia",
        "EF":"Finland",
        "EG":"United Kingdom",
        "EH":"Netherlands",
        "EI":"Ireland",
        "EK":"Denmark",
        "EL":"Luxembourg",
        "EN":"Norway",
        "EP":"Poland",
        "ES":"Sweden",
        "ET":"Germany",
        "EV":"Latvia",
        "EY":"Lithuania",
        "FA":"South Africa",
        "FB":"Botswana",
        "FC":"Republic of the Congo",
        "FD":"Swaziland",
        "FE":"Central African Republic",
        "FG":"Equatorial Guinea",
        "FH":"Ascension Island",
        "FI":"Mauritius",
        "FJ":"British Indian Ocean Territory",
        "FK":"Cameroon",
        "FL":"Zambia",
        "FM":"Comoros, Madagascar, Mayotte, Réunion",
        "FN":"Angola",
        "FO":"Gabon",
        "FP":"São Tomé and Príncipe",
        "FQ":"Mozambique",
        "FS":"Seychelles",
        "FT":"Chad",
        "FV":"Zimbabwe",
        "FW":"Malawi",
        "FX":"Lesotho",
        "FY":"Namibia",
        "FZ":"Democratic Republic of the Congo",
        "GA":"Mali",
        "GB":"The Gambia",
        "GC":"Canary Islands",
        "GE":"Ceuta and Melilla",
        "GF":"Sierra Leone",
        "GG":"Guinea-Bissau",
        "GL":"Liberia",
        "GM":"Morocco",
        "GO":"Senegal",
        "GQ":"Mauritania",
        "GS":"Western Sahara",
        "GU":"Guinea",
        "GV":"Cape Verde",
        "HA":"Ethiopia",
        "HB":"Burundi",
        "HC":"Somalia",
        "HD":"Djibouti",
        "HE":"Egypt",
        "HF":"Djibouti",
        "HH":"Eritrea",
        "HK":"Kenya",
        "HL":"Libya",
        "HR":"Rwanda",
        "HS":"Sudan",
        "HT":"Tanzania",
        "HU":"Uganda",
        "K":"United States of America",
        "LA":"Albania",
        "LB":"Bulgaria",
        "LC":"Cyprus",
        "LD":"Croatia",
        "LE":"Spain",
        "LF":"France",
        "LG":"Greece",
        "LH":"Hungary",
        "LI":"Italy",
        "LJ":"Slovenia",
        "LK":"Czech Republic",
        "LL":"Israel",
        "LM":"Malta",
        "LN":"Monaco",
        "LO":"Austria",
        "LP":"Portugal",
        "LQ":"Bosnia and Herzegovina",
        "LR":"Romania",
        "LS":"Switzerland",
        "LT":"Turkey",
        "LU":"Moldova",
        "LV":"Gaza Strip",
        "LW":"Macedonia",
        "LX":"Gibraltar",
        "LY":"Serbia and Montenegro",
        "LZ":"Slovakia",
        "MB":"Turks and Caicos Islands",
        "MD":"Dominican Republic",
        "MG":"Guatemala",
        "MH":"Honduras",
        "MK":"Jamaica",
        "MM":"Mexico",
        "MN":"Nicaragua",
        "MP":"Panama",
        "MR":"Costa Rica",
        "MS":"El Salvador",
        "MT":"Haiti",
        "MU":"Cuba",
        "MW":"Cayman Islands",
        "MY":"Bahamas",
        "MZ":"Belize",
        "NC":"Cook Islands",
        "NF":"Fiji, Tonga",
        "NG":"Kiribati, Tuvalu",
        "NI":"Niue",
        "NL":"Wallis and Futuna",
        "NS":"Samoa, American Samoa",
        "NT":"French Polynesia",
        "NV":"Vanuatu",
        "NW":"New Caledonia",
        "NZ":"New Zealand, Antarctica",
        "OA":"Afghanistan",
        "OB":"Bahrain",
        "OE":"Saudi Arabia",
        "OI":"Iran",
        "OJ":"Jordan and the West Bank",
        "OK":"Kuwait",
        "OL":"Lebanon",
        "OM":"United Arab Emirates",
        "OO":"Oman",
        "OP":"Pakistan",
        "OR":"Iraq",
        "OS":"Syria",
        "OT":"Qatar",
        "OY":"Yemen",
        "PA":"Alaska",
        "PB":"Baker Island",
        "PC":"Kiribati",
        "PF":"Fort Yukon, Alaska",
        "PG":"Guam, Northern Marianas",
        "PH":"Hawaii",
        "PJ":"Johnston Atoll",
        "PK":"Marshall Islands",
        "PL":"Kiribati",
        "PM":"Midway Island",
        "PO":"Alaska",
        "PP":"Alaska",
        "PT":"Federated States of Micronesia, Palau",
        "PW":"Wake Island",
        "RC":"Republic of China (Taiwan)",
        "RJ":"Japan",
        "RK":"South Korea",
        "RO":"Japan",
        "RP":"Philippines",
        "SA":"Argentina",
        "SB":"Brazil",
        "SC":"Chile",
        "SD":"Brazil",
        "SE":"Ecuador",
        "SF":"Falkland Islands",
        "SG":"Paraguay",
        "SK":"Colombia",
        "SL":"Bolivia",
        "SM":"Suriname",
        "SN":"Brazil",
        "SO":"French Guiana",
        "SP":"Peru",
        "SS":"Brazil",
        "SU":"Uruguay",
        "SV":"Venezuela",
        "SW":"Brazil",
        "SY":"Guyana",
        "TA":"Antigua and Barbuda",
        "TB":"Barbados",
        "TD":"Dominica",
        "TF":"Guadeloupe",
        "TG":"Grenada",
        "TI":"U.S. Virgin Islands",
        "TJ":"Puerto Rico",
        "TK":"Saint Kitts and Nevis",
        "TL":"Saint Lucia",
        "TN":"Netherlands Antilles, Aruba",
        "TQ":"Anguilla",
        "TR":"Montserrat",
        "TT":"Trinidad and Tobago",
        "TU":"British Virgin Islands",
        "TV":"Saint Vincent and the Grenadines",
        "TX":"Bermuda",
        "UA":"Kazakhstan, Kyrgyzstan",
        "UB":"Azerbaijan",
        "UD":"Armenia",
        "UG":"Georgia",
        "UK":"Ukraine",
        "UM":"Belarus",
        "UT":"Tajikistan, Turkmenistan, Uzbekistan",
        "U":"Russia",
        "VA":"India",
        "VC":"Sri Lanka",
        "VD":"Cambodia",
        "VE":"India",
        "VG":"Bangladesh",
        "VH":"Hong Kong, China",
        "VI":"India",
        "VL":"Laos",
        "VM":"Macau, China",
        "VN":"Nepal",
        "VO":"India",
        "VQ":"Bhutan",
        "VR":"Maldives",
        "VT":"Thailand",
        "VV":"Vietnam",
        "VY":"Myanmar",
        "WA":"Indonesia",
        "WB":"Malaysia, Brunei",
        "WI":"Indonesia",
        "WM":"Malaysia",
        "WP":"Timor-Leste",
        "WQ":"Indonesia",
        "WR":"Indonesia",
        "WS":"Singapore",
        "Y":"Australia",
        "Z":"People's Republic of China",
        "ZK":"North Korea",
        "ZM":"Mongolia",
        }
        if strCode in dictCountry:
            return dictCountry[strCode]
        elif strCode[0:1] in dictCountry:
            return dictCountry[strCode[0:1]]
        else:
            return None     
         

file = open('C:\\DEV\\work\\data.x-plane.com\\work\\apt.dat', 'r')
fileCSV = open('C:\\DEV\\work\\data.x-plane.com\\work\\airports.csv', 'w')

bLastLineAirport=False
strLastLine=""

mapper = ICAOIATAMapper()

airports=[]

for line in file:
    #print line
    if bLastLineAirport==True and line.startswith('100'):
        airport=APTAirport()
        airport.strAirportLine=strLastLine.strip()
        airport.strRunwayLine=line.strip()
        airports.append(airport)
        bLastLineAirport=False
    else:
        bLastLineAirport=False
    
    if bLastLineAirport==False and line.startswith('1 '):
        strLastLine=line
        bLastLineAirport=True

count=0
for airport in airports:
    airport.process(mapper)
    if airport.valid==True:
        fileCSV.write (airport.toCSV()+"\n")
        count=count+1

print "Wrote " + str(count) + " airports to file"

fileCSV.close()

    

    
   