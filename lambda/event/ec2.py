from typing import Literal, Union

from pydantic import BaseModel, Field
from event.cloudtrail import CloudTrailEventBase


class CreateImageResponseElements(BaseModel):
    requestId: str
    imageId: str


class EBS(BaseModel):
    volumeSize: int
    deleteOnTermination: bool


class BlockDeviceMappingItem(BaseModel):
    deviceName: str
    ebs: EBS


class BlockDeviceMapping(BaseModel):
    items: list[BlockDeviceMappingItem]


class Tag(BaseModel):
    key: str
    value: str


class TagSpecificationSetItem(BaseModel):
    resourceType: str
    tags: list[Tag]


class TagSpecificationSet(BaseModel):
    items: list[TagSpecificationSetItem]


class CreateImageTagSpecificationSetItem(TagSpecificationSetItem):
    resourceType: Union[Literal["image"], Literal["snapshot"]]


class CreateImageTagSpecificationSet(TagSpecificationSet):
    items: list[CreateImageTagSpecificationSetItem]


class CreateImageRequestParameters(BaseModel):
    instanceId: str
    name: str
    noReboot: bool
    blockDeviceMapping: BlockDeviceMapping
    tagSpecificationSet: CreateImageTagSpecificationSet


class CreateImageEvent(CloudTrailEventBase):
    eventName: Literal["CreateImage"]
    eventSource: Literal["ec2.amazonaws.com"]
    requestParameters: CreateImageRequestParameters
    responseElements: CreateImageResponseElements


class RunInstanceEvent(CloudTrailEventBase):
    eventName: Literal["RunInstance"]
    eventSource: Literal["ec2.amazonaws.com"]
    requestParameters: CreateImageRequestParameters
    responseElements: CreateImageResponseElements
