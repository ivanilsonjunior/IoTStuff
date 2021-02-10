import logging
import asyncio
from aiocoap import *
import json
logging.basicConfig(level=logging.INFO)

class CoAPConnection:
    '''
    Classe para recuperar dados de um sensor que utilize CoAP.

    Attributes:
            host (str): Sensor Hostname
            resource(srt): remote CoAP resource
    '''
    def __init__(self,host,resource):
        self.host = host
        self.resource = resource
    
    @classmethod
    def fromResource(cls,res):
        '''
        Instancia um objeto a partir de um Json
            Parameters:
                res (str): Json
        '''
        return cls(**json.loads(res))

    def getResource(self):
        return self.getCoAPFloat()

    async def getRawCoAP(self):
        protocol = await Context.create_client_context()
        request = Message(code=GET, uri='coap://%s/%s' % (self.host,self.resource))
        try:
            response = await protocol.request(request).response
        except Exception as e:
            print('Failed to fetch resource:')
            print(e)
        else:
            return float(response.payload)

    def getCoAPFloat(self):
        return float(asyncio.get_event_loop().run_until_complete(self.getRawCoAP()))