import boto3
from efed_lib import report

session = boto3.session.Session(profile_name='sam')
c = session.get_credentials()
s3 = session.resource('s3')
sam_staged_bucket = s3.Bucket('sam-staged-inputs')


def upload_file(local, remote):
    report("{} -> {}".format(local, remote))
    try:
        sam_staged_bucket.upload_file(local, remote)
        exit()
    except Exception as e:
        raise e
