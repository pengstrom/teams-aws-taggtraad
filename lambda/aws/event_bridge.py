from enum import StrEnum
from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, Field


class CreateImageResponseElements(BaseModel):
    #     "requestId": "3578b088-b346-4814-802a-73a75f62b946",
    requestId: str
    #     "imageId": "ami-0a3716ae54ca4bd2a",
    imageId: str


class SessionIssuer(BaseModel):
    #             "type": "Role",
    type: str
    #             "principalId": "AROA53QW5XUZZ6Q46UEST",
    principalId: str
    #             "arn": "arn:aws:iam::952457084211:role/aws-reserved/sso.amazonaws.com/eu-west-1/AWSReservedSSO_AdministratorAccess_b74a4c021349e18c",
    arn: str
    #             "accountId": "952457084211",
    accountId: str
    #             "userName": "AWSReservedSSO_AdministratorAccess_b74a4c021349e18c",
    userName: str


class SessionAttributes(BaseModel):
    #             "creationDate": "2026-03-25T09:52:22Z",
    creationDate: str
    #             "mfaAuthenticated": "false",
    mfaAuthenticated: bool


class SessionContext(BaseModel):
    #         "sessionIssuer": {
    #             "type": "Role",
    #             "principalId": "AROA53QW5XUZZ6Q46UEST",
    #             "arn": "arn:aws:iam::952457084211:role/aws-reserved/sso.amazonaws.com/eu-west-1/AWSReservedSSO_AdministratorAccess_b74a4c021349e18c",
    #             "accountId": "952457084211",
    #             "userName": "AWSReservedSSO_AdministratorAccess_b74a4c021349e18c",
    #         },
    sessionIssuer: SessionIssuer
    #         "attributes": {
    #             "creationDate": "2026-03-25T09:52:22Z",
    #             "mfaAuthenticated": "false",
    #         },
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
    # type: Literal[UserType.UNKNOWN] = UserType.UNKNOWN
    arn: Optional[str] = None
    accountId: Optional[str] = None
    accessKeyId: Optional[str] = None


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
    ],
    Field(discriminator="type"),
]


class UserIdentity2(BaseModel):
    #     "type": "AssumedRole",
    type: UserType
    #     "principalId": "AROA53QW5XUZZ6Q46UEST:per.engstrom@nwise.se",
    principalId: str
    #     "arn": "arn:aws:sts::952457084211:assumed-role/AWSReservedSSO_AdministratorAccess_b74a4c021349e18c/per.engstrom@nwise.se",
    arn: str
    #     "accountId": "952457084211",
    accountId: str
    #     "accessKeyId": "ASIA53QW5XUZX7CGCILC",
    accessKeyId: str
    #     "sessionContext": {
    #         "sessionIssuer": {
    #             "type": "Role",
    #             "principalId": "AROA53QW5XUZZ6Q46UEST",
    #             "arn": "arn:aws:iam::952457084211:role/aws-reserved/sso.amazonaws.com/eu-west-1/AWSReservedSSO_AdministratorAccess_b74a4c021349e18c",
    #             "accountId": "952457084211",
    #             "userName": "AWSReservedSSO_AdministratorAccess_b74a4c021349e18c",
    #         },
    #         "attributes": {
    #             "creationDate": "2026-03-25T09:52:22Z",
    #             "mfaAuthenticated": "false",
    #         },
    #     },
    sessionContext: SessionContext


class EBS(BaseModel):
    #                 "ebs": {"volumeSize": 100, "deleteOnTermination": True},
    volumeSize: int
    deleteOnTermination: bool


class BlockDeviceMappingItem(BaseModel):
    #                 "deviceName": "/dev/sda1",
    deviceName: str
    #                 "ebs": {"volumeSize": 100, "deleteOnTermination": True},
    ebs: EBS


class BlockDeviceMapping(BaseModel):
    items: list[BlockDeviceMappingItem]


class Tag(BaseModel):
    key: str
    value: str


class TagSpecificationSetItem(BaseModel):
    #                 "resourceType": "image",
    resourceType: str
    #                 "tags": [
    #                     {"key": "Foo", "value": "bar"},
    #                     {"key": "baz", "value": "  Quuz"},
    #                 ],
    tags: list[Tag]


class TagSpecificationSet(BaseModel):
    items: list[TagSpecificationSetItem]


class CreateImageRequestParameters(BaseModel):
    #     "instanceId": "i-0eb658a9365c53ad1",
    instanceId: str
    #     "name": "peen.nwise.se-test-tagg",
    name: str
    #     "noReboot": True,
    noReboot: bool
    #     "blockDeviceMapping": {
    #         "items": [
    #             {
    #                 "deviceName": "/dev/sda1",
    #                 "ebs": {"volumeSize": 100, "deleteOnTermination": True},
    #             }
    #         ]
    #     },
    blockDeviceMapping: BlockDeviceMapping
    #     "tagSpecificationSet": {
    #         "items": [
    #             {
    #                 "resourceType": "image",
    #                 "tags": [
    #                     {"key": "Foo", "value": "bar"},
    #                     {"key": "baz", "value": "  Quuz"},
    #                 ],
    #             },
    #             {
    #                 "resourceType": "snapshot",
    #                 "tags": [
    #                     {"key": "Foo", "value": "bar"},
    #                     {"key": "baz", "value": "  Quuz"},
    #                 ],
    #             },
    #         ]
    #     },
    tagSpecificationSet: TagSpecificationSet


class TlsDetails(BaseModel):
    #     "tlsVersion": "TLSv1.3",
    tlsVersion: str
    #     "cipherSuite": "TLS_AES_128_GCM_SHA256",
    cipherSuite: str
    #     "clientProvidedHostHeader": "ec2.eu-north-1.amazonaws.com",
    clientProvidedHostHeader: str


class AWSAPICallViaCloudTrail(BaseModel):
    # "eventVersion": "1.11",
    eventVersion: str
    # "userIdentity": {
    #     "type": "AssumedRole",
    #     "principalId": "AROA53QW5XUZZ6Q46UEST:per.engstrom@nwise.se",
    #     "arn": "arn:aws:sts::952457084211:assumed-role/AWSReservedSSO_AdministratorAccess_b74a4c021349e18c/per.engstrom@nwise.se",
    #     "accountId": "952457084211",
    #     "accessKeyId": "ASIA53QW5XUZX7CGCILC",
    #     "sessionContext": {
    #         "sessionIssuer": {
    #             "type": "Role",
    #             "principalId": "AROA53QW5XUZZ6Q46UEST",
    #             "arn": "arn:aws:iam::952457084211:role/aws-reserved/sso.amazonaws.com/eu-west-1/AWSReservedSSO_AdministratorAccess_b74a4c021349e18c",
    #             "accountId": "952457084211",
    #             "userName": "AWSReservedSSO_AdministratorAccess_b74a4c021349e18c",
    #         },
    #         "attributes": {
    #             "creationDate": "2026-03-25T09:52:22Z",
    #             "mfaAuthenticated": "false",
    #         },
    #     },
    # },
    userIdentity: UserIdentity
    # "eventTime": "2026-03-25T16:30:25Z",
    eventTime: str
    # "eventSource": "ec2.amazonaws.com",
    eventSource: str
    # "eventName": "CreateImage",
    eventName: str
    # "awsRegion": "eu-north-1",
    awsRegion: str
    # "sourceIPAddress": "13.53.34.220",
    sourceIPAddress: str
    # "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0",
    userAgent: str
    # "requestParameters": {
    #     "instanceId": "i-0eb658a9365c53ad1",
    #     "name": "peen.nwise.se-test-tagg",
    #     "noReboot": True,
    #     "blockDeviceMapping": {
    #         "items": [
    #             {
    #                 "deviceName": "/dev/sda1",
    #                 "ebs": {"volumeSize": 100, "deleteOnTermination": True},
    #             }
    #         ]
    #     },
    #     "tagSpecificationSet": {
    #         "items": [
    #             {
    #                 "resourceType": "image",
    #                 "tags": [
    #                     {"key": "Foo", "value": "bar"},
    #                     {"key": "baz", "value": "  Quuz"},
    #                 ],
    #             },
    #             {
    #                 "resourceType": "snapshot",
    #                 "tags": [
    #                     {"key": "Foo", "value": "bar"},
    #                     {"key": "baz", "value": "  Quuz"},
    #                 ],
    #             },
    #         ]
    #     },
    # },
    requestParameters: CreateImageRequestParameters
    # "responseElements": {
    #     "requestId": "3578b088-b346-4814-802a-73a75f62b946",
    #     "imageId": "ami-0a3716ae54ca4bd2a",
    # },
    responseElements: CreateImageResponseElements
    # "requestID": "3578b088-b346-4814-802a-73a75f62b946",
    requestID: str
    # "eventID": "ba9b5666-0ceb-4c4c-a733-f85ce183b2e3",
    eventID: str
    # "readOnly": False,
    readOnly: bool
    # "eventType": "AwsApiCall",
    eventType: str
    # "managementEvent": True,
    managementEvent: bool
    # "recipientAccountId": "952457084211",
    recipientAccountId: str
    # "eventCategory": "Management",
    eventCategory: str
    # "tlsDetails": {
    #     "tlsVersion": "TLSv1.3",
    #     "cipherSuite": "TLS_AES_128_GCM_SHA256",
    #     "clientProvidedHostHeader": "ec2.eu-north-1.amazonaws.com",
    # },
    tlsDetails: TlsDetails
    # "sessionCredentialFromConsole": "true",
    sessionCredentialFromConsole: bool
