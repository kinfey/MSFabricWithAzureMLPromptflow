from promptflow import tool
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azureml.fsspec import AzureMachineLearningFileSystem
from promptflow.connections import CustomConnection


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def load_md_data(files: str, azureml_conn:CustomConnection) -> str:

    credential = DefaultAzureCredential()

    ml_client = MLClient(
        credential, azureml_conn.AzureMLSubscription, azureml_conn.AzureMLResourceGroup, azureml_conn.AzureMLWorkspace
    )
    
    unstructured_data_asset = ml_client.data.get("md_files_demo", version="1.0.1")

    fs = AzureMachineLearningFileSystem(unstructured_data_asset.path)

    content = ''
    with fs.open('Files/docs/microsoft-fabric-overview.md') as f:
        content = f.read()
        f.close()

    md_content = content.decode("utf-8")

    content_start = md_content.index("# ")

    content_end = md_content.index("## Next steps")

    set_content = md_content[content_start:content_end]

    set_content = set_content.replace("\\","\\\\").replace("\"","\'").replace(":::","").replace("\n","")

    return set_content
