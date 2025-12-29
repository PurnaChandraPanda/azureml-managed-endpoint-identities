import os
import logging
import json
import numpy
import joblib
import requests
from azure.identity import ManagedIdentityCredential
from azure.storage.blob import BlobServiceClient, ContentSettings
from logging_config import configure_logger

## Setup the logger
_logger = configure_logger(__name__)

def init():
    # print env
    _logger.info(">>> ")
    _logger.info(os.system("printenv"))
    _logger.info(" <<<")

    global model, container_client
    # AZUREML_MODEL_DIR is an environment variable created during deployment.
    # It is the path to the model folder (./azureml-models/$MODEL_NAME/$VERSION)
    # For multiple models, it points to the folder containing all deployed models (./azureml-models)
    # Please provide your model's folder name if there is one
    model_path = os.path.join(
        os.getenv("AZUREML_MODEL_DIR"), "model/sklearn_regression_model.pkl"
    )
    # deserialize the model file back into a sklearn model
    model = joblib.load(model_path)
    _logger.info("Model loaded")

    blob_url = f"https://mlws012181044126.blob.core.windows.net"
    blob_container_name = "test24"
    
    msi_client_id = os.getenv("UAI_CLIENT_ID")
    credential = ManagedIdentityCredential(client_id=msi_client_id)

    _logger.info("before get token")
    cred_token = credential.get_token("https://management.azure.com/.default")
    _logger.info(f"after get token: {msi_client_id} -> {cred_token}")
    
    # Access Azure resource (Blob storage) using system assigned identity token
    blob_service_client = BlobServiceClient(
            account_url=blob_url,
            credential=credential,
            logging_enable=True,
        )

    # Get blob container client
    container_client = blob_service_client.get_container_client(blob_container_name)
    _logger.info("Init complete")

def upload_blob(blob_name, blob_data):
    try:
        _logger.info(f"Preparing to upload blob, Blob: {blob_name}")
        payload_bytes = blob_data.encode("utf-8")
        _logger.info(f"Blob payload size (bytes): {len(payload_bytes)}")

        container_client.upload_blob(
            name=blob_name,
            data=payload_bytes,
            overwrite=True,
            content_settings=ContentSettings(content_type="application/json"),
            max_concurrency=1,
            timeout=60  # avoid indefinite hang
        )
        _logger.info(f"✅ Predictions uploaded to blob: {blob_name}")
    except Exception as e:
        _logger.error(f"⚠ Blob upload failed: {e}")

# note you can pass in multiple rows for scoring
def run(raw_data):
    _logger.info("Request received")
    data = json.loads(raw_data)["data"]
    data = numpy.array(data)
    
    predictions = model.predict(data)
    _logger.info("✅ Prediction completed.")
    
    # Upload predictions to Blob
    blob_payload = json.dumps({"predictions": predictions.tolist()})
    upload_blob("predictions.json", blob_payload)
    _logger.info("Request processed")
    return predictions.tolist()