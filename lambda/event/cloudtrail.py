from enum import StrEnum
from typing import Annotated, Literal, Optional, Union
from pydantic import BaseModel, Field


class SessionIssuer(BaseModel):
    type: str
    principalId: str
    arn: str
    accountId: str
    userName: str


class SessionAttributes(BaseModel):
    creationDate: str
    mfaAuthenticated: bool


class SessionContext(BaseModel):
    sessionIssuer: SessionIssuer
    attributes: SessionAttributes


class UserType(StrEnum):
    ROOT = "Root"
    ROLE = "Role"
    IAM_USER = "IAMUser"
    IDENTITY_CENTER_USER = "IdentityCenterUser"
    ASSUMED_ROLE = "AssumedRole"
    FEDERATED_USER = "FederatedUser"
    DIRECTORY = "Directory"
    AWS_ACCOUNT = "AWSAccount"
    AWS_SERVICE = "AWSService"
    UNKNOWN = "Unknown"


class UserIdentityBase(BaseModel):
    # type: str
    principalId: str
    arn: str
    accountId: str
    # type: Literal[UserType.UNKNOWN] = UserType.UNKNOWN
    # arn: Optional[str] = None
    # accountId: Optional[str] = None
    # accessKeyId: Optional[str] = None
    # sessionContext: Optional[SessionContext] = None
    pass


class RootUser(UserIdentityBase):
    type: Literal[UserType.ROOT] = UserType.ROOT
    userName: Optional[str] = None


class RoleUser(UserIdentityBase):
    type: Literal[UserType.ROLE] = UserType.ROLE


class IAMUser(UserIdentityBase):
    type: Literal[UserType.IAM_USER] = UserType.IAM_USER
    userName: str
    principalId: str


class AssumedRoleUser(UserIdentityBase):
    type: Literal[UserType.ASSUMED_ROLE] = UserType.ASSUMED_ROLE
    principalId: str


class FederatedUser(UserIdentityBase):
    type: Literal[UserType.FEDERATED_USER] = UserType.FEDERATED_USER


class DirectoryUser(UserIdentityBase):
    type: Literal[UserType.DIRECTORY] = UserType.DIRECTORY
    userName: Optional[str] = None


class AWSServiceUser(UserIdentityBase):
    type: Literal[UserType.AWS_SERVICE] = UserType.AWS_SERVICE


class AWSAccountUser(UserIdentityBase):
    type: Literal[UserType.AWS_ACCOUNT] = UserType.AWS_ACCOUNT


class IdentityCenterUser(UserIdentityBase):
    type: Literal[UserType.IDENTITY_CENTER_USER] = UserType.IDENTITY_CENTER_USER


UserIdentity = Annotated[
    Union[
        RootUser
        | IAMUser
        | AssumedRoleUser
        | IdentityCenterUser
        | AWSAccountUser
        | DirectoryUser
        | FederatedUser
        | AWSServiceUser
        | RoleUser
    ],
    Field(discriminator="type"),
]


class TlsDetails(BaseModel):
    tlsVersion: str
    cipherSuite: str
    clientProvidedHostHeader: str


class EventType(StrEnum):
    AWS_API_CALL = "AwsApiCall"
    AWS_SERVICE_EVENT = "AwsServiceEvent"
    AWS_CONSOLE_ACTION = "AwsConsoleAction"
    AWS_CONSOLE_SIGN_IN = "AwsConsoleSignIn"
    AWS_VPCE_EVENTS = "AwsVpceEvents"


class CloudTrailEventBase(BaseModel):
    eventTime: str
    eventID: str
    eventVersion: str
    userIdentity: UserIdentity
    eventSource: str
    awsRegion: str
    sourceIPAddress: str
    recipientAccountId: str
    additionalEventData: Optional[dict] = None
    requestID: Optional[str] = None
    eventType: EventType
    apiVersion: Optional[str] = None
    readOnly: Optional[bool] = None
    eventCategory: Literal["Management"] = "Management"
    userAgent: Optional[str] = None
    tlsDetails: Optional[TlsDetails] = None
