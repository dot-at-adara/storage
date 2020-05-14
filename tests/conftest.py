import pytest


@pytest.fixture(scope='session', )
def test_directory():
    import os
    return os.path.abspath(__file__).replace('conftest.py', '')


@pytest.fixture(scope='session', )
def app_settings(test_directory):
    from stratus_api.core.settings import get_app_settings
    import os
    return get_app_settings(env_folder=os.path.join(test_directory, 'mocks/settings'))


@pytest.fixture(scope="session")
def local_hash_email_file():
    from hashlib import sha256
    from os.path import join
    import csv
    local_path = join('tests/mocks', 'local_email_ids.csv')
    with open(local_path, 'wt') as f:
        writer = csv.writer(f)
        writer.writerow(['id'])
        for record in [sha256(str(i).encode('utf-8')).hexdigest() for i in range(10000)]:
            writer.writerow([record])
    return local_path


@pytest.fixture()
def gcs_hash_email_file(app_settings, local_hash_email_file):
    from framework.storage.gcs import upload_file_to_gcs, delete_file_from_gcs
    from stratus_api.core.common import generate_random_id
    file_path = 'tests/mocks/{0}.csv'.format(generate_random_id())
    upload_file_to_gcs(local_path=local_hash_email_file, bucket_name=app_settings['test_bucket_name'],
                       file_path=file_path)
    yield dict(bucket_name=app_settings['test_bucket_name'], file_path=file_path)
    delete_file_from_gcs(bucket_name=app_settings['test_bucket_name'], file_path=file_path)
