def test_upload_file_to_gcs(app_settings, local_hash_email_file):
    from framework.storage.gcs import upload_file_to_gcs, get_filenames_by_pattern, delete_file_from_gcs
    from stratus_api.core.common import generate_random_id
    file_path = 'test/files/{0}.csv'.format(generate_random_id())
    upload_file_to_gcs(local_path=local_hash_email_file, file_path=file_path)
    files = get_filenames_by_pattern(bucket_name=app_settings['test_bucket_name'], file_path=file_path)
    assert len(files) == 1
    delete_file_from_gcs(bucket_name=app_settings['test_bucket_name'], file_path=file_path)
    files = get_filenames_by_pattern(bucket_name=app_settings['test_bucket_name'], file_path=file_path)
    assert len(files) == 0


def test_download_from_gcs(gcs_hash_email_file):
    from framework.storage.gcs import download_from_storage
    import csv
    local_file_path = download_from_storage(bucket_name=gcs_hash_email_file['bucket_name'],
                                            file_path=gcs_hash_email_file['file_path'])
    with open(local_file_path, 'rt') as f:
        reader = csv.DictReader(f)
        assert len([i for i in reader]) == 10000


def test_file_exist_in_gcs(gcs_hash_email_file):
    from framework.storage.gcs import check_file_exist_in_gcs
    file = check_file_exist_in_gcs(bucket_name=gcs_hash_email_file['bucket_name'],
                                   file_path=gcs_hash_email_file['file_path'])
    assert file
