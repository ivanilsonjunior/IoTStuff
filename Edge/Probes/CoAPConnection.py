import logging
import asyncio
from aiocoap import *
import json
logging.basicConfig(level=logging.INFO)

class CoAPConnection:
    def __init__(self,host,resource):
        self.host = host
        self.resource = resource
    
    @classmethod
    def fromResource(cls,res):
        return cls(**json.loads(res))# - Se os atributos tiverem as mesmas chaves

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
#            print('Result: %s\n%r'%(response.code, response.payload))

    def getCoAPFloat(self):
        return float(asyncio.get_event_loop().run_until_complete(self.getRawCoAP()))
#async def main():
#EdgeApp = getCoAP('localhost','/Sensing/Temp')

#if __name__ == "__main__":
#EdgeApp = asyncio.get_event_loop().run_until_complete(getCoAP('localhost','Sensing/Temp'))

#conn = CoAPConnection('localhost','Sensing/Temp')

#print (conn.getCoAPFloat())
