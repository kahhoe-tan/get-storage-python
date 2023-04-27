import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ResourceNotFoundError
from azure.mgmt.storage import StorageManagementClient

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/{resource_group}/{storage_account}")
def get_storage_account(resource_group: str, storage_account: str):
    try:
        default_credential = DefaultAzureCredential()
        load_dotenv()
        subscription_id = os.getenv('SUBSCRIPTION_ID')
        storage_client = StorageManagementClient(
            credential = default_credential,
            subscription_id = subscription_id
        )
        account = storage_client.storage_accounts.get_properties(
            account_name = storage_account,
            resource_group_name = resource_group
        )
        return account
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/{resource_group}/{storage_account}/containers")
def list_storage_account_containers(resource_group: str, storage_account: str):
    try:
        default_credential = DefaultAzureCredential()
        load_dotenv()
        subscription_id = os.getenv('SUBSCRIPTION_ID')
        storage_client = StorageManagementClient(
            credential = default_credential,
            subscription_id = subscription_id
        )
        containers = storage_client.blob_containers.list(
            account_name = storage_account,
            resource_group_name = resource_group,
        )
        resp_containers = []
        for container in containers:
            resp_containers.append(container.name)
        return resp_containers
    except ResourceNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))