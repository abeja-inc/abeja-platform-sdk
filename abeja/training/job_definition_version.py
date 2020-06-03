from typing import cast, Any, Dict, List, Optional, Union, IO, AnyStr
import io
from .api.client import APIClient
from .common import SizedIterable
from abeja.common.docker_image_name import DockerImageName
from . import job_definition


# Entity class


class JobDefinitionVersion():
    """Training job definition version object.
    """

    def __init__(self, api: APIClient,
                 organization_id: str,
                 job_definition_id: str,
                 job_definition_version_id: int,
                 handler: str,
                 image: DockerImageName,
                 environment: Dict[str, str],
                 description: str,
                 archived: bool,
                 created_at: str,
                 modified_at: str,
                 job_definition: Optional['job_definition.JobDefinition'] = None) -> None:
        self.__api = api
        self.__organization_id = organization_id
        self.__job_definition_id = job_definition_id
        self.__job_definition_version_id = job_definition_version_id
        self.__handler = handler
        self.__image = image
        self.__environment = environment
        self.__description = description
        self.__archived = archived
        self.__created_at = created_at
        self.__modified_at = modified_at
        self.__job_definition = job_definition

    @classmethod
    def from_response(klass, api: APIClient,
                      organization_id: str,
                      response: Dict[str, Any],
                      job_definition: Optional['job_definition.JobDefinition'] = None) -> 'JobDefinitionVersion':
        """Construct an object from API response.

        NOTE: For convenient, this method DOES NOT validate the input response and
        always returns an object filled with default values.
        """
        return klass(
            api=api,
            organization_id=organization_id,
            job_definition_id=response.get('job_definition_id', ''),
            job_definition_version_id=response.get('job_definition_version', 0),
            handler=response.get('handler', ''),
            image=DockerImageName.parse(str(response.get('image'))),
            environment=(response.get('environment') or {}),
            description=response.get('description', ''),
            archived=bool(response.get('archived')),
            created_at=response.get('created_at', ''),
            modified_at=response.get('modified_at', ''),
            job_definition=job_definition)

    @property
    def job_definition(self) -> 'job_definition.JobDefinition':
        if self.__job_definition is None:
            self.__job_definition = job_definition.JobDefinitions(
                api=self.__api, organization_id=self.organization_id).get(
                name=self.job_definition_id)
        return self.__job_definition

    @property
    def organization_id(self) -> str:
        """Get the organization ID of this job definition version."""
        return self.__organization_id

    @property
    def job_definition_id(self) -> str:
        """Get the job_definition ID of this job definition version."""
        return self.__job_definition_id

    @property
    def job_definition_version_id(self) -> int:
        """Get the version of this job definition version."""
        return self.__job_definition_version_id

    @property
    def handler(self) -> str:
        """Get the handler of this job definition version."""
        return self.__handler

    @property
    def image(self) -> DockerImageName:
        """Get the :class:`DockerImageName` of this job definition version."""
        return self.__image

    @property
    def environment(self) -> Dict[str, str]:
        """Get the environment variables of this job definition version."""
        return self.__environment

    @property
    def description(self) -> str:
        """Get the description of this job definition version."""
        return self.__description

    @property
    def archived(self) -> bool:
        """Get whether this job definition is archived or not."""
        return self.__archived

    @property
    def created_at(self) -> str:
        """Get the created date string (ISO 8601) of this job definition version."""
        return self.__created_at

    @property
    def modified_at(self) -> str:
        """Get the modified date string (ISO 8601) of this job definition version."""
        return self.__modified_at


class JobDefinitionVersions():
    """The training job definition version adapter class.
    """

    def __init__(
            self,
            api: APIClient,
            job_definition: 'job_definition.JobDefinition') -> None:
        self.__api = api
        self.__job_definition = job_definition

    @property
    def organization_id(self) -> str:
        """Get the organization ID."""
        return self.__job_definition.organization_id

    @property
    def job_definition_id(self) -> str:
        """Get the job definition ID."""
        return self.__job_definition.job_definition_id

    @property
    def job_definition_name(self) -> str:
        """Get the job definition name."""
        return self.__job_definition.name

    def get(self, job_definition_version_id: int) -> JobDefinitionVersion:
        """Get a training job definition version.

        Request Syntax:
            .. code-block:: python

                version = versions.get(job_definition_version_id=5)

        Params:
            - **job_definition_version_id** (int): the version number

        Return type:
            :class:`JobDefinitionVersion` object

        """
        res = self.__api.get_training_job_definition_version(
            organization_id=self.organization_id,
            job_definition_name=self.job_definition_name,
            version_id=job_definition_version_id)

        return JobDefinitionVersion.from_response(
            api=self.__api,
            organization_id=self.organization_id,
            response=res,
            job_definition=self.__job_definition)

    def list(
            self,
            filter_archived: Optional[bool] = None) -> SizedIterable[JobDefinitionVersion]:
        """Returns an iterator object that iterates training job definition versions
        under this object.

        This method returns an instance of :class:`SizedIterable`, so you can
        get the total number of training job definition versions.

        Params:
            - **filter_archived** (bool): **[optional]** If ``true``, include archived jobs, otherwise exclude archived jobs. (default: ``false``)

        Return type:
            SizedIterable[JobDefinitionVersion]
        """
        res = self.__api.get_training_job_definition_versions(
            organization_id=self.organization_id,
            job_definition_name=self.job_definition_name,
            filter_archived=filter_archived)

        versions = [
            JobDefinitionVersion.from_response(
                api=self.__api,
                organization_id=self.organization_id,
                response=entry,
                job_definition=self.__job_definition)
            for entry in res['entries']]
        # Because the SizedIterator<T> is not a true "Intersection Type" but is
        # a new class, a list object will not be considered as adapted.
        return cast(SizedIterable[JobDefinitionVersion], versions)

    def create(self,
               source: Union[List[str], IO[AnyStr]],
               handler: str,
               image: DockerImageName,
               environment: Optional[Dict[str, Any]] = None,
               description: Optional[str] = None):
        """Create a new training job definition version.

        Request Syntax:
            .. code-block:: python

                from abeja.common.docker_image_name import ALL_GPU_19_10

                version = versions.create(
                    source=['train.py'],
                    handler='train:handler',
                    image=ALL_GPU_19_10,
                    environment={'key': 'value'},
                    description='new version')

        Params:
            - **source** (List[str] | IO): an input source for training code. It's one of:
              - zip or tar.gz archived file-like object.
              - a list of file paths.
            - **image** (DockerImageName): runtime environment
            - **environment** (Optional[dict]): user defined parameters set as environment variables
            - **description** (Optional[str]): description

        Return type:
            :class:`JobDefinitionVersion` object

        """
        if isinstance(source, io.IOBase):
            parameters = {'handler': handler,
                          'image': str(image)}  # type: Dict[str, Any]

            if environment is not None:
                parameters['environment'] = environment
            if description is not None:
                parameters['description'] = description

            res = self.__api.create_training_job_definition_version_native_api(
                organization_id=self.organization_id,
                job_definition_name=self.job_definition_name,
                source_code=cast(IO[AnyStr], source),
                parameters=parameters)

            return JobDefinitionVersion.from_response(
                api=self.__api,
                organization_id=self.organization_id,
                response=res,
                job_definition=self.__job_definition)
        else:
            res = self.__api.create_training_job_definition_version(
                organization_id=self.organization_id,
                job_definition_name=self.job_definition_name,
                filepaths=cast(List[str], source),
                handler=handler,
                image=str(image),
                environment=environment,
                description=description)
            return JobDefinitionVersion.from_response(
                api=self.__api,
                organization_id=self.organization_id,
                response=res,
                job_definition=self.__job_definition)

    def update(self, job_definition_version_id: int,
               description: str) -> JobDefinitionVersion:
        """Update a training job definition version.

        Request Syntax:
            .. code-block:: python

                version = versions.update(job_definition_version_id=5, description='new version')

        Params:
            - **job_definition_version_id** (int): the version number

        Return type:
            :class:`JobDefinitionVersion` object

        """
        res = self.__api.patch_training_job_definition_version(
            organization_id=self.organization_id,
            job_definition_name=self.job_definition_name,
            version_id=job_definition_version_id,
            description=description)

        return JobDefinitionVersion.from_response(
            api=self.__api,
            organization_id=self.organization_id,
            response=res,
            job_definition=self.__job_definition)

    def archive(self, job_definition_version_id: int):
        """Archive a training job definition version.

        Request Syntax:
            .. code-block:: python

                versions.archive(job_definition_version_id=5)

        Params:
            - **job_definition_version_id** (int): the version number
        """
        self.__api.archive_training_job_definition_version(
            organization_id=self.organization_id,
            job_definition_name=self.job_definition_name,
            version_id=job_definition_version_id)

    def unarchive(self, job_definition_version_id: int):
        """Unarchive a training job definition version.

        Request Syntax:
            .. code-block:: python

                versions.unarchive(job_definition_version_id=5)

        Params:
            - **job_definition_version_id** (int): the version number
        """
        self.__api.unarchive_training_job_definition_version(
            organization_id=self.organization_id,
            job_definition_name=self.job_definition_name,
            version_id=job_definition_version_id)

    def delete(self, job_definition_version_id: int):
        """Delete a training job definition version.

        Request Syntax:
            .. code-block:: python

                versions.delete(job_definition_version_id=5)

        Params:
            - **job_definition_version_id** (int): the version number
        """
        self.__api.delete_training_job_definition_version(
            organization_id=self.organization_id,
            job_definition_name=self.job_definition_name,
            version_id=job_definition_version_id)
