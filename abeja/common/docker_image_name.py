from typing import Optional, NamedTuple
import re


__DockerImageName = NamedTuple('DockerImageName', [
    ('repository', str),
    ('name', str),
    ('tag', Optional[str]),
    ('host', Optional[str]),
])


class DockerImageName(__DockerImageName):
    """Docker image name possibly having tag and host.

    For detailed description about docker image name and tag, see
    https://docs.docker.com/engine/reference/commandline/tag/

    Naming rule for custom images
    -----------------------------

    Developers can register their custom image in ABEJA Platform.
    its name follows the rule below:

    - The host part of name is `custom`.
    - The repository part of name is the organization ID of a custom image.

    For example:

    ::

        custom/1234567890123/my-image:version1.0
    """
    @classmethod
    def custom_image(
            klass,
            organization_id: str,
            repository: str,
            tag: Optional[str]):
        return klass(organization_id, repository, tag, 'custom')

    @classmethod
    def parse(klass, value: str) -> 'DockerImageName':
        items = value.split('/', maxsplit=3)
        tag = None

        if len(items) == 2:
            host = None
            [repository, name] = items
        elif len(items) == 3:
            [host, repository, name] = items
        else:
            raise ValueError('invalid format: {}'.format(value))

        if ':' in name:
            [name, tag] = name.split(':', maxsplit=2)

        # validations
        if not re.fullmatch('\S+', repository):
            raise ValueError(
                'invalid format: repository={}'.format(repository))

        if not re.fullmatch('\S+', name):
            raise ValueError('invalid format: name={}'.format(name))

        if tag and not re.fullmatch('\S+', tag):
            raise ValueError('invalid format: tag={}'.format(tag))

        if host and not re.fullmatch('^[a-zA-Z0-9\._-]+(:\d+)?$', host):
            raise ValueError('invalid format: host={}'.format(host))

        return klass(repository=repository, name=name, tag=tag, host=host)

    def is_custom_image(self) -> bool:
        return self.host == 'custom'

    def organization_id(self) -> str:
        """Return the organization ID of this custom image."""
        return self.repository

    def __str__(self) -> str:
        name = '{}/{}'.format(self.host,
                              self.repository) if self.host else self.repository
        return '{}/{}:{}'.format(name,
                                 self.name,
                                 self.tag) if self.tag else '{}/{}'.format(name,
                                                                           self.name)


# Define pre-defined instance types
ALL_CPU_19_04 = DockerImageName.parse('abeja-inc/all-cpu:19.04')
ALL_CPU_19_10 = DockerImageName.parse('abeja-inc/all-cpu:19.10')
ALL_GPU_19_04 = DockerImageName.parse('abeja-inc/all-gpu:19.04')
ALL_GPU_19_10 = DockerImageName.parse('abeja-inc/all-gpu:19.10')
