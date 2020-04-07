# -*- coding: utf-8 -*-
import os
from pathlib import Path


def get_cache_dir():
    """return cache dir under home directory if possible,
    or return that under current directory"""
    try:
        return '{}/.abeja/.cache'.format(Path.home())
    except RuntimeError:
        return '{}/.cache'.format(os.getcwd())


# directory to save local files
MOUNT_DIR = os.environ.get('ABEJA_STORAGE_DIR_PATH', get_cache_dir())
DEFAULT_CHUNK_SIZE = 1 * 1024 * 1024    # 1MB
FETCH_WORKER_COUNT = int(os.environ.get('FETCH_WORKER_COUNT', 5))
UPLOAD_WORKER_COUNT = int(os.environ.get('UPLOAD_WORKER_COUNT', 5))
# chunksize of uploaded file to S3 by ARMS
S3_CHUNK_SIZE = 5 * 1024 * 1024
DOWNLOAD_RETRY_ATTEMPT_NUMBER = 3
