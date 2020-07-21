from mock import patch
import os
import shutil
from urllib.parse import urlparse

import pytest

from abeja.common.http_file import HTTPFile
from abeja.datasets.client import APIClient

TEST_MOUNT_DIR = "."
HTTP_URL = "http://example.com/a/b/c.jpg"
HTTP_URL_AND_PATH_PAIRS = (
    ("http://example.com/a/b/c.jpg",
     "{}/example.com/a/b/c.jpg".format(TEST_MOUNT_DIR)),
    ("https://example.com/1/2/3.jpg",
     "{}/example.com/1/2/3.jpg".format(TEST_MOUNT_DIR)),
    ("http://10.0.0.1:8080/a/b/c.jpg?x=123",
     "{}/10.0.0.1:8080/a/b/c.jpg".format(TEST_MOUNT_DIR)),
    ("http://localhost:30000/images/1.jpg?a=1&b=2",
     "{}/localhost:30000/images/1.jpg".format(TEST_MOUNT_DIR)))
HTTP_URLS = tuple(uri for uri, _ in HTTP_URL_AND_PATH_PAIRS)


def remove_all_cache_if_exist(uris):
    for uri in uris:
        remove_cache_if_exist(uri)


def remove_cache_if_exist(uri):
    o = urlparse(uri)
    if os.path.exists(o.netloc):
        shutil.rmtree(o.netloc)


class TestHTTPFile:
    def setup_method(self, method):
        remove_all_cache_if_exist(HTTP_URLS)

    def teardown_method(self, method):
        remove_all_cache_if_exist(HTTP_URLS)

    @patch("abeja.common.local_file.MOUNT_DIR", TEST_MOUNT_DIR)
    @pytest.mark.parametrize("uri,path", HTTP_URL_AND_PATH_PAIRS)
    def test_get_content_create_cache(self, requests_mock, uri, path):
        requests_mock.get(uri, text="abc")
        http_file = HTTPFile(api=APIClient(), uri=uri)
        assert http_file.get_content() == b"abc"
        assert os.path.exists(path)

    @patch("abeja.common.local_file.MOUNT_DIR", TEST_MOUNT_DIR)
    def test_get_content_from_cache(self):
        os.makedirs("./example.com/a/b")
        with open("./example.com/a/b/c.jpg", "wb") as f:
            f.write(b"abc")
        http_file = HTTPFile(api=APIClient(), uri=HTTP_URL)
        assert http_file.get_content() == b"abc"
