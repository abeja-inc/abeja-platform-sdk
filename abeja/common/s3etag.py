"""
The basic part of this function is copied from https://pypi.org/project/s3etag/.
s3etag was a command line tool, so I just cut it out as a function.
Original s3etag license is Apache License 2.0 .
"""
import hashlib


def calc_s3etag(target: bytes, chunk_size: int) -> str:
    """Compute Etag for a target"""
    mv = memoryview(target)
    count = 0
    pos = 0
    dgst_part = hashlib.md5()
    dgst_whole = hashlib.md5()
    while True:
        buf = mv[pos:(pos + chunk_size)]
        if len(buf) < 1:
            break
        count = count + 1
        pos += chunk_size
        dgst_part = hashlib.md5(buf)
        dgst_whole.update(dgst_part.digest())

    etag = "{}-{}".format(dgst_whole.hexdigest(),
                          count) if count > 1 else dgst_part.hexdigest()
    return etag
