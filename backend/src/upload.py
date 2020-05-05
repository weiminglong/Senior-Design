def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    from gcloud import storage
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))

if __name__ == '__main__':
    bucket = 'qaclassifier'
    file = 'audio/Mitochondria.flac'
    blob = 'Mitochondria.flac'
    upload_blob(bucket, file, blob)
