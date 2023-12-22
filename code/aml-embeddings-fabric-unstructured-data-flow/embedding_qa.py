
from openai import AzureOpenAI

from promptflow import tool
from promptflow.connections import AzureOpenAIConnection



def generate_embeddings(text: str, openai: AzureOpenAI):
    response = openai.embeddings.create(
        input=text, model="EmbeddingModel")
    embeddings = response.data[0].embedding
    return embeddings

@tool
def embedd_data(kb_list: dict,aoai_conn: AzureOpenAIConnection) -> dict: 
    # openai = OpenAI()
    # openai.api_type = 'azure'
    # openai.api_key = aoai_conn.api_key
    # openai.base_url = aoai_conn.api_base
    # openai.api_version = '2023-06-13-preview'
    openai = AzureOpenAI(
        azure_endpoint = aoai_conn.api_base, 
        api_key= aoai_conn.api_key,  
        api_version="2023-05-15"
    )
    i = 1000
    for item in kb_list:
        title = item['KB']
        content = item['Content']
        title_embeddings = generate_embeddings(title,openai)
        content_embeddings = generate_embeddings(content,openai)
        item["id"] = str(i)
        item['KBVector'] = title_embeddings
        item['ContentVector'] = content_embeddings
        i += 1
    return kb_list