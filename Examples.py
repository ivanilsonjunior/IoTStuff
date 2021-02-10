'''

Exemplos de utilização

''' 

import EdgeApp

#Session = sessionmaker(bind = engine)
#session = Session()
#result = session.query(Locations).all()

#for location in result:
#    print (location) 
#    for sensor in location.sensors:
#        print ("\t" + str(sensor))


# probe = session.query(Probes).filter_by(run=True).first()
#dei = session.query(Locations).filter_by(name='dei').first()
#print(dei)
#teste = Locations(name="DEEC")
#session.add(teste)
#session.commit()




#data = RawData()
#data.probe = probinho
#data.timestamp = datetime.now()
#data.data =  11.1
#session.add(data)
#session.commit()



# from sqlalchemy import func
#  med = session.query(func.avg(RawData.data)).filter(RawData.probe == probe).one()
# session.query(func.avg(RawData.data)).filter(RawData.probe == probe).filter(RawData.timestamp.between('2021-01-22','2021-01-23')).one()
if __name__ == '__main__':
    gerente = EdgeApp.Puppeteer("DataBase.db")