import os
import sys
import time
import datetime
import zipfile
import mimetypes
import shutil
from os import sep

import S3

import config

def zipit(file_path):
    zip_name = getZipFileName(zip_prefix)
    zip_file = file_path
    zip = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED)
    zip.write(file_name)
    zip.close()
     
    # File Operations #
    os.remove(file_name)
    mv_to_path = os.path.join(copy_dir, zip_name)
    mv_to_dir = sep.join(mv_to_path.split(sep)[:-1])
    if not os.access(mv_to_dir, os.F_OK):
        os.makedirs(mv_to_dir)
    if os.access(mv_to_path, os.F_OK):
        os.remove(mv_to_path)
    shutil.copy(zip_file, mv_to_path)
    return zip_name

def S3Upload(file_name, file_path, bucket_name):
    print 'uploading to aws s3'
    conn = S3.AWSAuthConnection(config.AWS_ACCESS_KEY_ID, config.AWS_SECRET_ACCESS_KEY)
    print 'conn', conn, '\n', dir(conn)
    File = open(file_path, 'rb')
    filedata = File.read()
    content_type = mimetypes.guess_type(file_path)[0]
    content_size = os.path.getsize(file_path)
    if not content_type:
        content_type = 'text/plain'
    print 'conn put'
    st = conn.put(bucket_name, file_name, S3.S3Object(filedata),
        {'x-amz-acl': 'public-read', 'Content-Type': content_type})
    print 'end conn put'
    resp = st.http_response
    print 'resp', resp, resp.status
    File.close()
    if 200 != resp.status:
        return False
    return True
