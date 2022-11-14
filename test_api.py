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
from fastapi.testclient import TestClient
from api import app
from model import StatusInfo, FeatureVectorSearchResult
import numpy as np
from time import sleep
import pytest

class TestVoldAPI(object):

    client = TestClient(app)
    vector = list(np.random.rand(768))

    @classmethod
    def setup_class(cls):

        response = cls.client.post("/upsert",
                        headers={"Content-Type": "application/json"},
                        json={"id":"test-ss1", "vector": cls.vector})    
        print(StatusInfo.parse_obj(response.json()))

        change3 = cls.vector[3:]
        changeVector1 = [0.1, 0.2, 0.2]        
        changeVector1[len(changeVector1):len(changeVector1)] = change3
        
        changeVector2 = [0.1, 0.9, 0.3]
        changeVector2[len(changeVector2):len(changeVector2)] = change3

        changeVector3 = [0.1, 0.2, 0.4]        
        changeVector3[len(changeVector3):len(changeVector3)] = change3

        changeVector4 = [0.11,0.22,0.39]        
        changeVector4[len(changeVector4):len(changeVector4)] = change3

        response = cls.client.post("/upsert",
                        headers={"Content-Type": "application/json"},
                        json={"id":"test-ms1", "vector": changeVector1})    
        assert response.status_code == 200
        response = cls.client.post("/upsert",
                        headers={"Content-Type": "application/json"},
                        json={"id":"test-ms2", "vector": changeVector2})    
        assert response.status_code == 200
        response = cls.client.post("/upsert",
                        headers={"Content-Type": "application/json"},
                        json={"id":"test-ms3", "vector": changeVector3})    
        assert response.status_code == 200
        response = cls.client.post("/upsert",
                        headers={"Content-Type": "application/json"},
                        json={"id":"test-ms4", "vector": changeVector3})    
        assert response.status_code == 200
        response = cls.client.post("/upsert",
                        headers={"Content-Type": "application/json"},
                        json={"id":"test-ms5", "vector": changeVector4})    
        assert response.status_code == 200
        
        sleep(90)

    @classmethod
    def teardown_class(cls):
        response = cls.client.post("/delete",
                            headers={"Content-Type": "application/json"},
                            json={"id":"test-ss1", "vector": []})        
        print(StatusInfo.parse_obj(response.json()))

        response = cls.client.post("/delete",
                            headers={"Content-Type": "application/json"},
                            json={"id":"test-ms1", "vector": []})        
        print(StatusInfo.parse_obj(response.json()))

        response = cls.client.post("/delete",
                            headers={"Content-Type": "application/json"},
                            json={"id":"test-ms2", "vector": []})        
        print(StatusInfo.parse_obj(response.json()))

        response = cls.client.post("/delete",
                            headers={"Content-Type": "application/json"},
                            json={"id":"test-ms3", "vector": []})        
        print(StatusInfo.parse_obj(response.json()))

        response = cls.client.post("/delete",
                            headers={"Content-Type": "application/json"},
                            json={"id":"test-ms4", "vector": []})        
        print(StatusInfo.parse_obj(response.json()))

        response = cls.client.post("/delete",
                            headers={"Content-Type": "application/json"},
                            json={"id":"test-ms5", "vector": []})        
        print(StatusInfo.parse_obj(response.json()))



        
        
    def test_EmptyVector(self):    
        response = self.client.post("/insert",
                            headers={"Content-Type": "application/json"},
                            json={"id":"test-empty", "vector": []})    
        assert response.status_code == 200
        statusInfo = StatusInfo.parse_obj(response.json())
        assert statusInfo.status == "ERROR"
        assert "Incompatible Dimension Size detected" in statusInfo.message

    
    def test_InsertEmptyVector(self):    
        response = self.client.post("/insert",
                            headers={"Content-Type": "application/json"},
                            json={"id":"test-empty", "vector": []})    
        assert response.status_code == 200
        statusInfo = StatusInfo.parse_obj(response.json())
        assert statusInfo.status == "ERROR"
        assert "Incompatible Dimension Size detected" in statusInfo.message

    def test_InsertEmptyId(self):    
        
        response = self.client.post("/insert",
                            headers={"Content-Type": "application/json"},
                            json={"id":"", "vector": self.vector})    
        assert response.status_code == 200
        statusInfo = StatusInfo.parse_obj(response.json())
        assert statusInfo.status == "ERROR"
        assert "UNKNOWN:Error" in statusInfo.message

    def test_InsertAndDelete(self):  
        
        response = self.client.post("/insert",
                            headers={"Content-Type": "application/json"},
                            json={"id":"test1", "vector": self.vector})    
        assert response.status_code == 200
        statusInfo = StatusInfo.parse_obj(response.json())
        assert statusInfo.status == "OK"
        assert "" in statusInfo.message
        
        response = self.client.post("/delete",
                            headers={"Content-Type": "application/json"},
                            json={"id":"test1", "vector": []})    
        assert response.status_code == 200
        statusInfo = StatusInfo.parse_obj(response.json())
        assert statusInfo.status == "OK"
        assert "" in statusInfo.message


    def test_SingleSearch(self):     

        response = self.client.post("/search",
                            headers={"Content-Type": "application/json"},
                            json={"vector": self.vector, "num":10, "radius":-1.0, "epsilon":0.01, "timeout": 50000000000})    
        assert response.status_code == 200
        searchResult = FeatureVectorSearchResult.parse_obj(response.json())
        assert searchResult.statusInfo.status == "OK"
        assert "" in searchResult.statusInfo.message
        assert searchResult.ids[0] == "test-ss1"

    def test_MultiSearch(self):     

        change3 = self.vector[3:]
        changeVector1 = [0.1, 0.2, 0.2]        
        changeVector1[len(changeVector1):len(changeVector1)] = change3

        changeVector3 = [0.1, 0.2, 0.4]        
        changeVector3[len(changeVector3):len(changeVector3)] = change3

        response = self.client.post("/multiSearch",
                            headers={"Content-Type": "application/json"},
                            json={"vectors": [{"vector":changeVector1}, {"vector":changeVector3}], "num":10, "radius":-1.0, "epsilon":0.01, "timeout": 50000000000})    
        assert response.status_code == 200
        searchResult = FeatureVectorSearchResult.parse_obj(response.json())
        assert searchResult.statusInfo.status == "OK"
        assert "" in searchResult.statusInfo.message
        assert sorted(list(set(searchResult.ids))) == ['test-ms1', 'test-ms3', 'test-ms4', 'test-ms5']
        

    def test_SearchById(self):     

        response = self.client.post("/searchById",
                            headers={"Content-Type": "application/json"},
                            json={"id":"test-ss1"})    
        assert response.status_code == 200
        searchResult = FeatureVectorSearchResult.parse_obj(response.json())
        assert searchResult.statusInfo.status == "OK"
        assert "" in searchResult.statusInfo.message
        assert searchResult.ids[0] == "test-ss1"
