#import subprocess
import random
from datetime import datetime
import importlib
# Probes
from Edge.Probes.CoAPConnection import CoAPConnection
from Edge.Probes.WAPIConnection import WAPIConnection
#
from sqlalchemy import create_engine, MetaData, ForeignKey, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy.orm import relationship
#Para realizar as alterações/consultas
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

class Locations(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    def __str__(self):
        return str(self.name + " has " + str(len(self.sensors)) + " sensors")

class Sensors(Base):
    __tablename__ = 'sensors'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    hostname = Column(String(50), nullable=False)
    active = Column(Boolean(), nullable=False)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    location = relationship("Locations", back_populates="sensors")
    def __str__(self):
        return str(self.name + " has " + str(len(self.probes)) + " probes")


class Probes(Base):
    __tablename__ = 'probes'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    cronMinute = Column(Integer, nullable=False)
    resource = Column(String(100), nullable=False)
    run = Column(String(50), nullable=False)
    sensor_id = Column(Integer, ForeignKey('sensors.id'))
    sensor = relationship("Sensors", back_populates="probes")
    datatype_id = Column(Integer, ForeignKey('datatypes.id'))
    datatype = relationship("DataTypes")
    commtype_id = Column(Integer, ForeignKey('commtypes.id'))
    commtype = relationship("CommTypes")
    
    def __str__(self):
        return str(self.name + " collects " + self.datatype.name + " for " + self.sensor.name + " using " + self.commtype.name)
    
    def getData(self, session):
        module = importlib.import_module('Edge.Probes.' + self.commtype.runCommand)
        probe = getattr(module, self.commtype.runCommand)
        collectedData = RawData()
        collectedData.probe = self 
        collectedData.timestamp = datetime.now()
        collectedData.data = probe.fromResource(self.resource).getResource()
        session.add(collectedData)
        session.commit()


class DataTypes(Base):
    __tablename__ = 'datatypes'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    unit = Column(String(50))
    isexception = Column(Boolean())

class CommTypes(Base):
    __tablename__ = 'commtypes'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    runCommand = Column(String(50), nullable=False)

class RawData(Base):
    __tablename__ = 'rawdata'
    id = Column(Integer, primary_key=True)
    data = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    probe_id = Column(Integer, ForeignKey('probes.id'))
    probe = relationship("Probes", back_populates="collecteddata")
    def __str__(self):
        return str(self.probe.name + " collected " + str(self.data) + self.probe.datatype.unit + " at " + str(self.timestamp))


Locations.sensors = relationship("Sensors", order_by = Sensors.id, back_populates="location")
Sensors.probes = relationship("Probes", order_by = Probes.id, back_populates="sensor")
Probes.collecteddata = relationship("RawData", order_by = RawData.id, back_populates="probe")


class Puppeteer():
    def __init__(self,dataBase):
        self.engine = create_engine('sqlite:///' + dataBase, echo = False)
        Session = sessionmaker(bind = self.engine)
        self.session = Session()
        self.meta = MetaData()
        if self.meta.is_bound():
            print("Ecziste")
        else:
            print("Non Ecziste")
        self.meta.create_all(self.engine)
        Base.metadata.create_all(self.engine)


    def addLocation(self, newName):
        newLoc = Locations(name = newName)
        self.session.add(newLoc)
        self.session.commit()

    def addSensor(self, newName, newHost, isActive, sensLocation):
        newSensor = Sensors(name = newName, hostname = newHost, active = isActive, location = sensLocation)
        self.session.add(newSensor)
        self.session.commit()

    def runProbes(self):
        activeSensors = self.session.query(Sensors).filter_by(active=True).all()
        for sens in activeSensors:
            for prob in sens.probes:
                if ((datetime.now().time().minute % prob.cronMinute) == 0 ):
                    prob.getData(self.session)

    def getProbeRawData(self,probe): 
        return self.session.query(RawData).filter(RawData.probe == probe)
        

    def  getProbeRawDataAvgByInterval(self,probe,start,end):
        return self.session.query(func.avg(RawData.data)).filter(RawData.probe == probe).filter(RawData.timestamp.between(start,end)).one()