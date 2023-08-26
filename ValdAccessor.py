'''
  Copyright 2021 Linked Ideal LLC.[https://linked-ideal.com/]
 
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
 
      http://www.apache.org/licenses/LICENSE-2.0
 
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
 '''

import grpc
from vald.v1.vald import insert_pb2_grpc
from vald.v1.vald import search_pb2_grpc
from vald.v1.vald import update_pb2_grpc
from vald.v1.vald import upsert_pb2_grpc
from vald.v1.vald import remove_pb2_grpc
from vald.v1.vald import object_pb2_grpc
from vald.v1.payload import payload_pb2
import os
from logging import config
config.fileConfig('logging.conf')
import logging
LOG = logging.getLogger(__name__)

class ValdAccessor():

    channel = None
    istub = None
    ustub = None
    usstub = None
    sstub = None
    rstub = None

    def __init__(self) :
        self.channel = grpc.insecure_channel(os.environ["TOPOSOID_VALD_HOST"] + ":" + os.environ["TOPOSOID_VALD_PORT"])
        ## create stubs for calling RPCs
        self.istub = insert_pb2_grpc.InsertStub(self.channel)
        self.ustub = update_pb2_grpc.UpdateStub(self.channel)
        self.usstub = upsert_pb2_grpc.UpsertStub(self.channel)
        self.sstub = search_pb2_grpc.SearchStub(self.channel)        
        self.rstub = remove_pb2_grpc.RemoveStub(self.channel)
        self.exstub = object_pb2_grpc.ObjectStub(self.channel)

    def insert(self, id, vector):
        vec = payload_pb2.Object.Vector(id=id, vector=vector)
        icfg = payload_pb2.Insert.Config(skip_strict_exist_check=True)
        self.istub.Insert(payload_pb2.Insert.Request(vector=vec, config=icfg))

    def upsert(self, id, vector):
        self.delete(id)      
        self.insert(id, vector)

        #Something is wrong
        #vec = payload_pb2.Object.Vector(id=id, vector=vector)
        #uscfg = payload_pb2.Upsert.Config(skip_strict_exist_check=False)
        #self.usstub.Upsert(payload_pb2.Upsert.Request(vector=vec, config=uscfg))

    def search(self, vector, num=10, radius=-1.0, epsilon=0.01, timeout=3000000000):
        scfg = payload_pb2.Search.Config(num=num, radius=radius, epsilon=epsilon, timeout=timeout)
        res = self.sstub.Search(payload_pb2.Search.Request(vector=vector, config=scfg))
        if len(res.results) == 0:
            return [], []
        else:
            result = []
            similarities = []
            for x in res.results:
                LOG.info(x.id + ": "+ str(x.distance))
                #if not getattr(x, 'distance'):
                #    result.append(x.id)
                #    similarities.append(1.0)
                if x.distance < float(os.environ["TOPOSOID_VALD_DISTANCE_THRESHHOLD"]) :
                    result.append(x.id)
                    if x.distance == 0:
                        similarities.append(1.0)
                    else:
                        similarities.append(1.0 - x.distance)
            return result, similarities        

            #return list(map(lambda x:  x.id, res.results))

    def multiSearch(self, vectors, num=10, radius=-1.0, epsilon=0.01, timeout=3000000000):
        scfg = payload_pb2.Search.Config(num=num, radius=radius, epsilon=epsilon, timeout=timeout)        
        reqs = list(map(lambda v: payload_pb2.Search.Request(vector=v.vector, config=scfg), vectors))        
        res = self.sstub.MultiSearch(payload_pb2.Search.MultiRequest(requests=reqs))        
        if len(res.responses) == 0:
            return [], []
        else:
            result = []
            similarities = []
            for x in res.responses:                                
                for y in x.results:
                    LOG.info(y.id + ": "+ str(y.distance))                    
                    #if not getattr(y, 'distance'):                        
                    #    result.append(y.id)
                    #    similarities.append(1.0)
                    if y.distance < float(os.environ["TOPOSOID_VALD_DISTANCE_THRESHHOLD"]) :
                        result.append(y.id)
                        if y.distance == 0:
                            similarities.append(1.0)
                        else:
                            similarities.append(1.0 - y.distance)                                      
            return result, similarities            

    def searchById(self, id):   
        try:     
            scfg = payload_pb2.Search.Config(num=1, radius=-1.0, epsilon=0.1, timeout=3000000000)
            res = self.sstub.SearchByID(payload_pb2.Search.IDRequest(id=id, config=scfg))
            if len(res.results) == 0:
                return [], []
            else:
                result = []
                similarities = []
                for x in res.results:
                    LOG.info(x.id + ": "+ str(x.distance))
                    #if not getattr(x, 'distance'):                        
                    #    result.append(x.id)
                    #    similarities.append(1.0)                     
                    if x.distance == 0.0:                        
                        result.append(x.id)
                        similarities.append(1.0)

                return result, similarities            
        except Exception as e:
            pass
            return [],[]


    def delete(self, id): 
        try:
            result = self.exstub.Exists(payload_pb2.Object.ID(id=id))
            rcfg = payload_pb2.Remove.Config(skip_strict_exist_check=True)
            rid = payload_pb2.Object.ID(id=id)
            self.rstub.Remove(payload_pb2.Remove.Request(id=rid, config=rcfg))
        except Exception as e:
            pass
     
