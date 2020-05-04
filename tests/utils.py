import random
import uuid


def random_hex(n):
    return '%030x' % random.randrange((n * 2)**30)


def fake_platform_id():
    """Generates pseudo ABEJA Platform ID (e.g. "1335799549456")"""
    return '1' + ''.join([str(random.randint(0, 9)) for x in range(0, 12)])


def fake_iso8601():
    return '{}-{:02}-{:02}T{:02}:{:02}:{:02}+00:00'.format(
        random.randint(1996, 2020),
        random.randint(1, 12),
        random.randint(1, 30),
        random.randint(0, 23),
        random.randint(0, 59),
        random.randint(0, 59))


def fake_file_id():
    return '{}{:02}{:02}T{:02}{:02}{:02}-{}'.format(
        random.randint(1996, 2020),
        random.randint(1, 12),
        random.randint(1, 30),
        random.randint(0, 23),
        random.randint(0, 59),
        random.randint(0, 59),
        uuid.uuid4()
    )
