# Download compensation.json for a given assessment and athlete video
# eg: gs://videos/2-Leg-Squat-Front-1234-9087/compensations.json
import os
import pathlib
import json
from google.cloud import storage
import shutil
from compensation_models import CompensationDatabaseModel

PARENT_BLOB_FOLDER = 'videos'

def createFolder(folder_name):
    parent_directory = pathlib.Path.cwd()
    full_folder_path = pathlib.Path.home().joinpath(
        parent_directory,
        folder_name
    )
    try:
        os.makedirs(full_folder_path)
    except:
        print(f"Folder path '{full_folder_path}' already exists")

def removeFolder(folder_name):
    parent_directory = pathlib.Path.cwd()
    full_folder_path = pathlib.Path.home().joinpath(
        parent_directory,
        folder_name
    )
    try:
        shutil.rmtree(str(full_folder_path))
    except:
        print(f"Folder path '{full_folder_path}' can't be deleted")


def bucketFileDownloader(bucket_name, prefix, output_folder_name='output'):
    """
    bucket_name: fusionetics-raw-data-jan
    prefix: subfolder such as 'videos'
    folder_name: 2-Leg-Squat-Front_1234-45y9
    compensations.json for the corresponding folder 
    gets downloaded
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)
    for blob in blobs:
        if blob.name.endswith('compensations.json'):
            folder_name = blob.name.split('/')[1]
            assessment_type, video_id = folder_name.split('_')
            print(assessment_type, ':', video_id)
            # TODO: check if the folder exists in the database

            # if not
            createFolder(output_folder_name)
            output_file_path = pathlib.Path.home().joinpath(
                pathlib.Path.cwd(),
                output_folder_name,
                'compensations.json'
            )
            blob.download_to_filename(output_file_path)
            # call curv parser
            return 0

bucketFileDownloader('fusionetics-raw-data-jan', 'videos')