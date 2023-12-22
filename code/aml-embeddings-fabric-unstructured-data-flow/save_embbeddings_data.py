from promptflow import tool
from promptflow.connections import CognitiveSearchConnection

from azure.core.credentials import AzureKeyCredential  
from azure.search.documents import SearchClient  
from azure.search.documents.indexes import SearchIndexClient  



from azure.search.documents.indexes.models import (  
    SearchIndex,  
    SearchField,  
    SearchFieldDataType,  
    SimpleField,  
    SearchableField,  
    SemanticConfiguration,  
    SemanticField,  
    VectorSearch,
    HnswAlgorithmConfiguration,
    SemanticPrioritizedFields,
    SemanticSearch,
    VectorSearchAlgorithmMetric,
    VectorSearchProfile,
    VectorSearchAlgorithmKind,
    HnswParameters
) 


def initSearch(service_endpoint : str ,index_name: str,credential: AzureKeyCredential):
  # Create a search index
  index_client = SearchIndexClient(
      endpoint=service_endpoint, credential=credential)
  fields = [
      SimpleField(name="id", type=SearchFieldDataType.String, key=True, sortable=True, filterable=True, facetable=True),
      SearchableField(name="KB", type=SearchFieldDataType.String),
      SearchableField(name="Content", type=SearchFieldDataType.String),
      SearchField(name="KBVector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                  searchable=True, vector_search_dimensions=1536, vector_search_profile_name="myHnswProfile"),
      SearchField(name="ContentVector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                  searchable=True, vector_search_dimensions=1536, vector_search_profile_name="myHnswProfile"),
  ]

    # Configure the vector search configuration  
  vector_search = VectorSearch(
        algorithms=[
            HnswAlgorithmConfiguration(
                name="myHnsw",
                kind=VectorSearchAlgorithmKind.HNSW,
                parameters=HnswParameters(
                    m=4,
                    ef_construction=400,
                    ef_search=500,
                    metric=VectorSearchAlgorithmMetric.COSINE
                )
            )
        ],
        profiles=[
            VectorSearchProfile(
                name="myHnswProfile",
                algorithm_configuration_name="myHnsw",
            )
        ]
    )

  semantic_config = SemanticConfiguration(
      name="my-semantic-config",
      prioritized_fields=SemanticPrioritizedFields(
          title_field=SemanticField(field_name="KB"),
          content_fields=[SemanticField(field_name="Content")]
      )
  )

  semantic_search = SemanticSearch(configurations=[semantic_config])


  index = SearchIndex(name=index_name, fields=fields,
                      vector_search=vector_search, semantic_search=semantic_search)
  result = index_client.create_or_update_index(index)

@tool
def save_data_embeddings(vector_json: dict, cogconn: CognitiveSearchConnection) -> str:
    documents = vector_json 
    service_endpoint = cogconn.api_base
    index_name = 'promptindex'
    key = cogconn.api_key
    credential = AzureKeyCredential(key)
    initSearch(service_endpoint,index_name,credential)

    search_client = SearchClient(endpoint=service_endpoint, index_name=index_name, credential=credential)
    result = search_client.upload_documents(documents) 
    return 'done'