import requests
from datetime import datetime
import collections
import json


class WAPIConnection:
    '''
    Classe para recuperar dados de clima do OpenWeatherMap
    Attributes:
            apiKEY (str): OpenWeatherMap API key
            cityId(srt): Target City Id
    '''
    def __init__(self, apiKEY, cityID):
        self.apiKey = apiKEY
        self.cityId = cityID
        self.objWeather = self.getWeatherData()
        self.conditions = { "Condition":[ 
    { "id": 200, "main":"Thunderstorm", "description":"thunderstorm with light rain", "icon":"11d"},
    { "id": 201, "main":"Thunderstorm", "description":"thunderstorm with rain", "icon":"11d"},
    { "id": 202, "main":"Thunderstorm", "description":"thunderstorm with heavy rain", "icon":"11d"},
    { "id": 210, "main":"Thunderstorm", "description":"light thunderstorm rain", "icon":"11d"},    
    { "id": 211, "main":"Thunderstorm", "description":"thunderstorm", "icon":"11d"},
    { "id": 212, "main":"Thunderstorm", "description":"heavy thunderstorm", "icon":"11d"},    
    { "id": 221, "main":"Thunderstorm", "description":"ragged thunderstorm", "icon":"11d"},
    { "id": 230, "main":"Thunderstorm", "description":"thunderstorm with light drizzle", "icon":"11d"},
    { "id": 231, "main":"Thunderstorm", "description":"thunderstorm with drizzle", "icon":"11d"},
    { "id": 232, "main":"Thunderstorm", "description":"thunderstorm with heavy drizzle", "icon":"11d"},

    { "id": 300, "main":"Drizzle", "description":"light intensity drizzle", "icon":"09d"},
    { "id": 301, "main":"Drizzle", "description":"drizzle", "icon":"09d"},
    { "id": 302, "main":"Drizzle", "description":"heavy intensity drizzle", "icon":"09d"},
    { "id": 310, "main":"Drizzle", "description":"light intensity drizzle rain", "icon":"09d"},
    { "id": 311, "main":"Drizzle", "description":"drizzle rain", "icon":"09d"},
    { "id": 312, "main":"Drizzle", "description":"heavy intensity drizzle rain", "icon":"09d"},
    { "id": 313, "main":"Drizzle", "description":"shower rain and drizzle", "icon":"09d"},
    { "id": 314, "main":"Drizzle", "description":"heavy shower rain and drizzle", "icon":"09d"},
    { "id": 321, "main":"Drizzle", "description":"shower drizzle", "icon":"09d"},

    { "id": 500, "main":"Rain", "description":"light rain", "icon":"10d"},
    { "id": 501, "main":"Rain", "description":"moderate rain", "icon":"10d"},
    { "id": 502, "main":"Rain", "description":"heavy intensity rain", "icon":"10d"},
    { "id": 503, "main":"Rain", "description":"very heavy rain", "icon":"10d"},
    { "id": 504, "main":"Rain", "description":"extreme rain", "icon":"10d"},
    { "id": 511, "main":"Rain", "description":"freezing rain", "icon":"13d"},
    { "id": 520, "main":"Rain", "description":"light intensity shower rain", "icon":"09d"},
    { "id": 521, "main":"Rain", "description":"shower rain", "icon":"09d"},
    { "id": 522, "main":"Rain", "description":"heavy intensity shower rain", "icon":"09d"},
    { "id": 531, "main":"Rain", "description":"ragged shower drizzle", "icon":"09d"},
    
    { "id": 600, "main":"Snow", "description":"light snow", "icon":"13d"},    
    { "id": 601, "main":"Snow", "description":"snow", "icon":"13d"},
    { "id": 602, "main":"Snow", "description":"heavy snow", "icon":"13d"},
    { "id": 611, "main":"Snow", "description":"sleet", "icon":"13d"},
    { "id": 612, "main":"Snow", "description":"light shower sleet", "icon":"13d"},        
    { "id": 613, "main":"Snow", "description":"shower sleet", "icon":"13d"},
    { "id": 615, "main":"Snow", "description":"light rain and snow", "icon":"13d"},    
    { "id": 616, "main":"Snow", "description":"rain and snow", "icon":"13d"},    
    { "id": 620, "main":"Snow", "description":"light shower snow", "icon":"13d"},
    { "id": 621, "main":"Snow", "description":"shower snow", "icon":"13d"},
    { "id": 622, "main":"Snow", "description":"heavy shower snow", "icon":"13d"},
    
    { "id": 701, "main":"Mist", "description":"mist", "icon":"50d"},
    { "id": 711, "main":"Smoke", "description":"smoke", "icon":"50d"},
    { "id": 721, "main":"Haze", "description":"haze", "icon":"50d"},
    { "id": 731, "main":"Dust", "description":"sand/dust whirls", "icon":"50d"},
    { "id": 741, "main":"Fog", "description":"fog", "icon":"50d"},
    { "id": 751, "main":"Sand", "description":"sand", "icon":"50d"},
    { "id": 761, "main":"Dust", "description":"dust", "icon":"50d"},
    { "id": 762, "main":"Ash", "description":"vulcanic ash", "icon":"50d"},
    { "id": 771, "main":"Squall", "description":"squalls", "icon":"50d"},
    { "id": 781, "main":"Tornado", "description":"tornado", "icon":"50d"},
    
    { "id": 800, "main":"Clear", "description":"clear sky", "icon":"01d,01n"},
    
    { "id": 801, "main":"Clouds", "description":"few clouds: 11-25%", "icon":"02d,02n"},
    { "id": 802, "main":"Clouds", "description":"scattered clouds: 25-50%", "icon":"03d,03n"},
    { "id": 803, "main":"Clouds", "description":"broken clouds: 51-84%", "icon":"04d,04n"},
    { "id": 804, "main":"Clouds", "description":"overcast clouds: 85-100%", "icon":"04d,04n"}

    ]  }
                
    @classmethod
    def fromResource(cls,res): #TODO: Alterar o json de entrada
        #return cls(**res) - Se os atributos tiverem as mesmas chaves
        resource = json.loads(res)
        cls.method = resource['method']
        return cls(resource['apikey'],resource['city'])
     
    def getResource(self):
        return getattr(self,self.method)()
        
    def getWeatherData(self):
        weather_url = 'http://api.openweathermap.org/data/2.5/weather?appid={key}&units=metric&id={cityid}'.format(key=self.apiKey.rstrip(), cityid=self.cityId.rstrip())
        jsonData = requests.get(weather_url).json()
        chaves = jsonData.keys()
        valores = jsonData.values()
        def criaWeather(self):
            return collections.namedtuple('weatherData', chaves)(* valores)
        return json.loads(json.dumps(jsonData), object_hook=criaWeather)

    def getTemperature(self):
        return float(self.objWeather.main['temp'])

    def getHumidity(self):
        return float(self.objWeather.main['humidity'])

    def getDateTime(self):
        return datetime.fromtimestamp(self.objWeather.dt)
    
    def getCondition(self):
        return self.getConditionById(self.objWeather.weather[0]['id'])

    def getConditionById(self, idCond):
        for cond in self.conditions['Condition']:
            if cond['id'] == idCond:
                return json.loads(json.dumps(cond), object_hook=lambda c: SimpleNamespace(**c))
        raise Exception("Condition.ID not found.")