import pytest
from abeja.common.docker_image_name import DockerImageName, ALL_CPU_19_04, ALL_CPU_19_10, ALL_GPU_19_04, ALL_GPU_19_10


POSSIBLE_DOCKER_IMAGES = [
    (ALL_CPU_19_04,
     'abeja-inc/all-cpu:19.04'),
    (ALL_CPU_19_10,
     'abeja-inc/all-cpu:19.10'),
    (ALL_GPU_19_04,
     'abeja-inc/all-gpu:19.04'),
    (ALL_GPU_19_10,
     'abeja-inc/all-gpu:19.10'),
    (DockerImageName(
        'fedora',
        'httpd',
        'version1.0',
        None),
        'fedora/httpd:version1.0'),
    (DockerImageName(
        'fedora',
        'httpd',
        'version1.0',
        'myregistryhost:5000'),
     'myregistryhost:5000/fedora/httpd:version1.0'),
    (DockerImageName(
        'fedora',
        'httpd',
        None,
        None),
     'fedora/httpd'),
]


@pytest.mark.parametrize('expected,value', POSSIBLE_DOCKER_IMAGES)
def test_parse(value: str, expected: DockerImageName) -> None:
    name = DockerImageName.parse(value)
    assert name == expected
    assert str(name) == value


def test_tag() -> None:
    name = DockerImageName('fedora', 'httpd', 'version1.0', None)
    assert name.repository == 'fedora'
    assert name.name == 'httpd'
    assert name.tag == 'version1.0'


def test_without_tag() -> None:
    name = DockerImageName('fedora', 'httpd', None, None)
    assert name.repository == 'fedora'
    assert name.name == 'httpd'
    assert name.tag is None


def test_with_host() -> None:
    name = DockerImageName(
        'fedora',
        'httpd',
        'version1.0',
        'myregistryhost:5000')
    assert name.repository == 'fedora'
    assert name.name == 'httpd'
    assert name.tag == 'version1.0'
    assert name.host == 'myregistryhost:5000'


def test_cusotm_image() -> None:
    organization_id = '1234567890123'
    repository_name = 'myimage'
    name = DockerImageName.custom_image(
        organization_id, repository_name, 'version1.0')

    assert str(
        name) == 'custom/{}/{}:version1.0'.format(organization_id, repository_name)
    assert name.is_custom_image()
