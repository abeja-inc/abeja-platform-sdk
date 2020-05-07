from typing import NamedTuple


__JobStatus = NamedTuple('InstanceType', [
    ('value', str),
])


class JobStatus(__JobStatus):
    """Set of job statuses which indicates a job is pending, running or
    failed and what ever.

    - **PENDING**: Necessary resources for running job is currently prepared
    - **ACTIVE**: The job is actively running
    - **STOPPED**: The job was stopped by user
    - **COMPLETE**: The job was successfully completed
    - **FAILED**: The job was failed by some reason
    """

    def __str__(self) -> str:
        return self.value


PENDING = JobStatus('Pending')
ACTIVE = JobStatus('Active')
STOPPED = JobStatus('Stopped')
COMPLETE = JobStatus('Complete')
FAILED = JobStatus('Failed')
