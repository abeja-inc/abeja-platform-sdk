from enum import Enum


class JobStatus(Enum):
    """Set of job statuses which indicates a job is pending, running or
    failed and what ever.

    - **PENDING**: Necessary resources for running job is currently prepared
    - **ACTIVE**: The job is currently running
    - **STOPPED**: The job was stopped by user
    - **COMPLETE**: The job was successfully completed
    - **FAILED**: The job was failed by some reason
    - **UNKNOWN**: Unrecognized value
    """
    PENDING = 'Pending'
    ACTIVE = 'Active'
    STOPPED = 'Stopped'
    COMPLETE = 'Complete'
    FAILED = 'Failed'
    UNKNOWN = 'unknown'

    @staticmethod
    def from_value(value: str) -> 'JobStatus':
        """Get a member by ``value`` if exists, otherwise return ``UNKNOWN``."""
        try:
            return JobStatus(value)
        except ValueError:
            return JobStatus.UNKNOWN
