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

from pydantic import BaseModel
from typing import List


#For searching feature vectors.
class FeatureVectorForUpdate(BaseModel):
    id:str
    vector:List[float]

#For deleting feature vectors
class FeatureVectorId(BaseModel):
    id:str

#For searching feature vectors.
class FeatureVectorForSearch(BaseModel):
    vector:List[float]

#For feature vector search requests
class SingleFeatureVectorForSearch(BaseModel):
    vector:List[float]
    num:int
    radius:float
    epsilon:float
    timeout:int

#For feature vector search requests. Multiple vectors can be set.
class MultiFeatureVectorForSearch(BaseModel):
    vectors:List[FeatureVectorForSearch]
    num:int
    radius:float
    epsilon:float
    timeout:int

#Status Information
class StatusInfo(BaseModel):
    status:str
    message:str

#For feature vector search results
class FeatureVectorSearchResult(BaseModel):
    ids:List[str]
    statusInfo:StatusInfo