import pytest


@pytest.fixture()
def sftp_key_client(app_settings):
    from framework.storage.sftp import connect_ssh_client_with_key
    return connect_ssh_client_with_key(
        key_filename=app_settings['test_sftp_key_filename'], hostname=app_settings['test_sftp_hostname'],
        username=app_settings['test_sftp_username'], password=app_settings['test_sftp_password']
    )


def test_get_list_of_files_by_pattern(app_settings, sftp_key_client):
    """ Test if the list of file paths that match the wildcard string are returned successfully. """
    from framework.storage.sftp import get_list_of_files_by_pattern
    list_of_matched_files = get_list_of_files_by_pattern(
        ssh=sftp_key_client, remote_dir_path=app_settings['test_sftp_remote_dir_path'],
        file_pattern=app_settings['test_sftp_file_pattern']
    )
    assert list_of_matched_files


def test_download_remote_file(app_settings, sftp_key_client):
    """ Test if the remote file is downloaded successfully. """
    from framework.storage.sftp import download_remote_file
    import os
    download_remote_file(
        ssh=sftp_key_client, remote_file_path=app_settings['test_sftp_remote_file_path'],
        local_dir_path=app_settings['test_sftp_local_dir_path']
    )
    assert os.path.isfile(app_settings['test_sftp_local_dir_path'] + app_settings['test_sftp_remote_file'])


def test_upload_local_file(app_settings, sftp_key_client, local_hash_email_file):
    """ Test if the local file is uploaded to the key path in specified bucket successfully. """
    from framework.storage.sftp import upload_local_file
    result = upload_local_file(
        ssh=sftp_key_client, upload_dir_path=app_settings['test_sftp_upload_dir_path'],
        local_file_path=local_hash_email_file
    )
    assert result
