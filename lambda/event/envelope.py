from typing import Annotated, Literal, Optional, Union
from pydantic import BaseModel, Field
from enum import StrEnum, auto

from event.ec2 import *


class DetailType(StrEnum):
    AWS_API_CALL_VIA_CLOUDTRAIL = "AWS API Call via CloudTrail"
    UNKNOWN = "UNKNOWN"


EventBridgeEventDetail = Annotated[
    Union[CreateImageEvent | RunInstanceEvent], Field(discriminator="eventName")
]


class EventBridgeEvent(BaseModel):
    account: str
    detail_type: Literal[DetailType.AWS_API_CALL_VIA_CLOUDTRAIL] = (
        DetailType.AWS_API_CALL_VIA_CLOUDTRAIL
    )
    detail: EventBridgeEventDetail
    get_id: str
    raw_event: str
    region: str
    replay_name: str
    resources: list
    source: str
    time: str
    version: str
