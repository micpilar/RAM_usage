#Program monitoruje zużycie pamięci RAM w czasie rzeczywistym i przesyła wyniki do Azure Blob Storage do pliku ram_usage.txt

import psutil
import time
import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

#Funkcja zwracająca zużycie pamięci RAM w GB
def get_ram_usage():
    return psutil.psutil.virtual_memory().used/(1024**3)

#Funkcja rozpoczynająca połączenie z Azure Blob Storage
def establish_connection():
    load_dotenv()
    connection_string=os.getenv('AZURE_CONNECTION_STRING')
    try:
        blob_service_client=BlobServiceClient.from_connection_string(connection_string)
    except Exception as e:
        print(e)
    return blob_service_client

#Funkcja przesyłające dane do Azure Blob Storage
def upload_data(blob_service_client, data):
    try:
        container_client=blob_service_client.get_container_client('data')
        blob_client=container_client.get_blob_client('ram_usage.txt')
        blob_client.upload_blob(data)
    except Exception as e:
        print(e)

def main():
    blob_service_client=establish_connection()
    while True:
        ram_usage=get_ram_usage()
        upload_data(blob_service_client,str(ram_usage))
        time.sleep(1)