import tempfile
import zipfile
from unittest import TestCase

from abeja.common.file_helpers import convert_to_zipfile_object, convert_to_valid_path


class TestFileHelpers(TestCase):
    def test_convert_to_zipfile_object(self):
        with tempfile.NamedTemporaryFile() as tf:
            tf.write("dummy".encode('utf-8'))
            tf.seek(0)
            rtn = convert_to_zipfile_object(tf)
            self.assertTrue(zipfile.is_zipfile(rtn.name))

        with tempfile.NamedTemporaryFile() as tf:
            tf.write("dummy".encode('utf-8'))
            tf.seek(0)
            tmp_file = tempfile.NamedTemporaryFile(suffix='.zip')
            with zipfile.ZipFile(tmp_file.name, 'w', compression=zipfile.ZIP_DEFLATED) as new_zip:
                new_zip.write(tf.name)
                rtn = convert_to_zipfile_object(tmp_file)
                self.assertTrue(zipfile.is_zipfile(rtn.name))

    def test_convert_to_valid_path(self):
        filepath = 'dummy/dummy.data'
        self.assertEqual(filepath, str(convert_to_valid_path(filepath)))

        filepath = '/dummy/dummy.data'
        self.assertNotEqual(filepath, str(convert_to_valid_path(filepath)))

        filepath = 'dummy/../dummy.data'
        self.assertNotEqual(filepath, str(convert_to_valid_path(filepath)))
