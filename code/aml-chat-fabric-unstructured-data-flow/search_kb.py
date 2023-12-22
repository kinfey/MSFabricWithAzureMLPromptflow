from typing import List
from promptflow import tool
from promptflow.connections import CognitiveSearchConnection

from azure.core.credentials import AzureKeyCredential  
from azure.search.documents import (
    SearchClient
)  

from azure.search.documents.models import VectorizedQuery 


@tool
def search_kb(questionvector: List[float],cogconn: CognitiveSearchConnection) -> str:

  search_client = SearchClient(cogconn.api_base, 'promptindex', credential=AzureKeyCredential(cogconn.api_key))
  vector_query = VectorizedQuery(vector=questionvector, k_nearest_neighbors=3, fields="KBVector,ContentVector")  
    
  results = search_client.search(  
      search_text=None,  
      vector_queries= [vector_query],
      select=["KB", "Content"],
  )  
  
  result_item = ''

  for result in results:  
      result_item = result['Content']
      break

  return result_item
