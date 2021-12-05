import boto3

import settings


def s3_download_file(s3_path: str, file_name: str) -> str:
    local_path = f'./{file_name}'
    s3 = boto3.resource('s3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    aws_session_token=settings.AWS_SESSION_TOKEN)
    bucket = s3.Bucket(settings.BUCKET)
    bucket.download_file(s3_path,
                         local_path)
    return local_path


def s3_upload_file(local_path: str, file_name: str) -> str:
    s3_path = f'files/{file_name}'
    s3 = boto3.resource('s3',
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                    aws_session_token=settings.AWS_SESSION_TOKEN)
    bucket = s3.Bucket(settings.BUCKET)
    bucket.upload_file(local_path, s3_path)
    return s3_path

def delete_s3_file(file_path: str) -> bool:        
    try:
        s3_path = f'{file_path}'
        s3 = boto3.client("s3")
        s3.delete_object(Bucket=settings.BUCKET, Key=s3_path)
        return True
    except:
        return False