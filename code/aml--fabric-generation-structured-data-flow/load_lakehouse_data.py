from promptflow import tool

from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from promptflow.connections import CustomConnection

@tool
def load_lakehouse_path(file: str , azureml_conn:CustomConnection) -> str:

    credential = DefaultAzureCredential()

    ml_client = MLClient(
        credential, azureml_conn.AzureMLSubscription, azureml_conn.AzureMLResourceGroup, azureml_conn.AzureMLWorkspace
    )
    
    data_asset = ml_client.data.get("structured_data", version="1.0.0")

    return data_asset.path +  file


    # data_path = azureml_conn.AzureMLData

    # load_structured_data = Data(
    #     path=data_path,
    #     type=AssetTypes.URI_FOLDER,
    #     description="structured data",
    #     name="structured_data",
    #     version="1.0.0"
    # )

    # ml_client.data.create_or_update(load_structured_data)
    # return 'OK'
