import pytest


@pytest.fixture()
def s3_credentials(app_settings):
    return dict(bucket_name=app_settings['test_bucket_name'], aws_access_key_id=app_settings['test_s3_access_key_id'],
                aws_secret_access_key=app_settings['test_s3_secret_access_key'],
                aws_session_token=app_settings['test_s3_session_token'])


def test_get_file_paths_by_pattern(app_settings, s3_credentials):
    """ Test if the list of file paths that match the wildcard string are returned successfully. """
    from framework.storage.s3 import get_list_of_files_by_pattern
    list_of_matched_files = get_list_of_files_by_pattern(file_pattern=app_settings['test_s3_file_pattern'],
                                                         **s3_credentials)
    assert list_of_matched_files


def test_download_remote_file(app_settings, s3_credentials):
    """ Test if the remote file is downloaded successfully. """
    from framework.storage.s3 import download_remote_file
    import os
    download_remote_file(remote_file_path=app_settings['test_s3_remote_file_path'],
                         local_dir_path=app_settings['test_s3_local_dir_path'], **s3_credentials)
    assert os.path.isfile(app_settings['test_s3_local_dir_path'] + app_settings['test_s3_remote_file_path'])


def test_upload_local_file(app_settings, s3_credentials, local_hash_email_file):
    """ Test if the local file is uploaded to the key path in specified bucket successfully. """
    from framework.storage.s3 import upload_local_file
    result = upload_local_file(local_file_path=app_settings['test_s3_local_file_path'],
                               remote_dir_path=app_settings['test_s3_remote_dir_path'], **s3_credentials)
    assert result
