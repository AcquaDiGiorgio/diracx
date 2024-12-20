# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator (autorest: 3.10.0, generator: @autorest/python@6.26.0)
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from enum import Enum
from azure.core import CaseInsensitiveEnumMeta


class ChecksumAlgorithm(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """ChecksumAlgorithm."""

    SHA256 = "sha256"


class Enum0(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Response Type."""

    CODE = "code"


class Enum1(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Code Challenge Method."""

    S256 = "S256"


class Enum2(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Enum2."""

    AUTHORIZATION_CODE = "authorization_code"


class Enum3(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Enum3."""

    URN_IETF_PARAMS_OAUTH_GRANT_TYPE_DEVICE_CODE = (
        "urn:ietf:params:oauth:grant-type:device_code"
    )


class Enum4(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Enum4."""

    REFRESH_TOKEN = "refresh_token"


class JobStatus(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """JobStatus."""

    SUBMITTING = "Submitting"
    RECEIVED = "Received"
    CHECKING = "Checking"
    STAGING = "Staging"
    WAITING = "Waiting"
    MATCHED = "Matched"
    RUNNING = "Running"
    STALLED = "Stalled"
    COMPLETING = "Completing"
    DONE = "Done"
    COMPLETED = "Completed"
    FAILED = "Failed"
    DELETED = "Deleted"
    KILLED = "Killed"
    RESCHEDULED = "Rescheduled"


class SandboxFormat(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """SandboxFormat."""

    TAR_BZ2 = "tar.bz2"


class SandboxType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Sandbox Type."""

    INPUT = "input"
    OUTPUT = "output"


class ScalarSearchOperator(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """ScalarSearchOperator."""

    EQ = "eq"
    NEQ = "neq"
    GT = "gt"
    LT = "lt"
    LIKE = "like"


class SortDirection(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """SortDirection."""

    ASC = "asc"
    DESC = "desc"


class VectorSearchOperator(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """VectorSearchOperator."""

    IN = "in"
    NOT_IN = "not in"
