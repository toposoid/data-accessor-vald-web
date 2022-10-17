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
from model import VectorInfo, ValdSearchInfo, StatusInfo, ValdSearchResult
import pytest

class TestVoldAPI(object):

    client = TestClient(app)

    def setup_method(self,method):
        print('method={}'.format(method.__name__))
        response = self.client.post("/delete",
                            headers={"Content-Type": "application/json"},
                            json={"id":"test1", "vector": []})        
        print(StatusInfo.parse_obj(response.json()))
        response = self.client.post("/delete",
                            headers={"Content-Type": "application/json"},
                            json={"id":"test2", "vector": []})        
        print(StatusInfo.parse_obj(response.json()))
        response = self.client.post("/delete",
                            headers={"Content-Type": "application/json"},
                            json={"id":"test3", "vector": []})        
        print(StatusInfo.parse_obj(response.json()))
        response = self.client.post("/delete",
                            headers={"Content-Type": "application/json"},
                            json={"id":"test4", "vector": []})        
        print(StatusInfo.parse_obj(response.json()))
        response = self.client.post("/delete",
                            headers={"Content-Type": "application/json"},
                            json={"id":"test5", "vector": []})        
        print(StatusInfo.parse_obj(response.json()))


    def teardown_method(self, method):
        print('method={}'.format(method.__name__))
        
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
                            json={"id":"", "vector": [0.1, 0.2, 0.3]})    
        assert response.status_code == 200
        statusInfo = StatusInfo.parse_obj(response.json())
        assert statusInfo.status == "ERROR"
        assert "empty uuid" in statusInfo.message

    def test_InsertAndDelete(self):  
        
        response = self.client.post("/insert",
                            headers={"Content-Type": "application/json"},
                            json={"id":"test1", "vector": [0.1, 0.2, 0.3]})    
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

        response = self.client.post("/insert",
                        headers={"Content-Type": "application/json"},
                        json={"id":"test2", "vector": [0.1, 0.2, 0.3]})    
        assert response.status_code == 200
        statusInfo = StatusInfo.parse_obj(response.json())
        assert statusInfo.status == "OK"
        assert "" in statusInfo.message
        
        response = self.client.post("/search",
                            headers={"Content-Type": "application/json"},
                            json={"vector": [0.1, 0.2, 0.3], "num":10, "radius":-1.0, "epsilon":0.01, "timeout": 50000000000})    
        assert response.status_code == 200
        searchResult = ValdSearchResult.parse_obj(response.json())
        assert searchResult.statusInfo.status == "OK"
        assert "" in searchResult.statusInfo.message
        assert searchResult.ids[0] == "test2"

    def test_MultiSearch(self):     

        response = self.client.post("/insert",
                        headers={"Content-Type": "application/json"},
                        json={"id":"test1", "vector": [0.1, 0.2, 0.2]})    
        assert response.status_code == 200
        response = self.client.post("/upsert",
                        headers={"Content-Type": "application/json"},
                        json={"id":"test2", "vector": [0.1, 0.2, 0.3]})    
        assert response.status_code == 200
        response = self.client.post("/upsert",
                        headers={"Content-Type": "application/json"},
                        json={"id":"test3", "vector": [0.1, 0.2, 0.4]})    
        assert response.status_code == 200
        response = self.client.post("/upsert",
                        headers={"Content-Type": "application/json"},
                        json={"id":"test4", "vector": [0.1, 0.2, 0.4]})    
        assert response.status_code == 200
        response = self.client.post("/upsert",
                        headers={"Content-Type": "application/json"},
                        json={"id":"test5", "vector": [0.11,0.22,0.39]})    
        assert response.status_code == 200
        
        
        response = self.client.post("/multiSearch",
                            headers={"Content-Type": "application/json"},
                            json={"vectors": [{"vector":[0.1,0.2,0.2]}, {"vector":[0.1,0.2,0.4]}], "num":10, "radius":-1.0, "epsilon":0.01, "timeout": 50000000000})    
        assert response.status_code == 200
        searchResult = ValdSearchResult.parse_obj(response.json())
        assert searchResult.statusInfo.status == "OK"
        assert "" in searchResult.statusInfo.message
        assert searchResult.ids == ['test1', 'test4', 'test3', 'test5']
        