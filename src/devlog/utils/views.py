import os
from typing import List, Optional
from urllib.parse import urljoin, urlparse

from flask import current_app, request, session, url_for
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


def next_redirect(fallback_endpoint: str, *args, **kwargs) -> str:
    """Find redirect url. The order of search is request params, session and
    finally url for fallback endpoint is returned if none found. Args and
    kwargs are passed intact to endpoint.

    :param fallback_endpoint: full endpoint specification
    :type fallback_endpoint: str
    :return: HTTP path to redirect to
    :rtype: str
    """
    for c in [request.args.get('next'), session.pop('next', None)]:
        if is_redirect_safe(c):
            return c
    return url_for(fallback_endpoint, *args, **kwargs)


def is_redirect_safe(target: Optional[str]) -> bool:
    """Check if redirect is safe, that is using HTTP protocol and is pointing
    to the same site.

    :param target: redirect target url
    :type target: str
    :return: flag signalling whether redirect is safe
    :rtype: bool
    """
    if not target:
        return False
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def valid_files(files: List[FileStorage]) -> List:
    """Retrieve list of valid file storage objects from request data.

    :param files: list of file uploads
    :type files: List[FileStorage]
    :return: list of valid file names
    :rtype: List
    """
    valid_files = []
    for fs in files:
        if fs.filename != '' and \
                fs.filename.endswith(current_app.config['ALLOWED_UPLOAD_EXTENSIONS']):
            valid_files.append(fs)
    return valid_files


def path_for_file_upload(fs: FileStorage) -> str:
    """Generate path where uploaded file should be saved.

    :param fs: file upload object
    :type fs: FileStorage
    :return: file system path to save uploaded file
    :rtype: str
    """
    file_name = secure_filename(fs.filename)
    upload_dir = os.path.join(
        current_app.instance_path, current_app.config['UPLOAD_DIR_NAME']
    )
    return os.path.join(upload_dir, file_name)
