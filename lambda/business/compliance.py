from typing import Optional

from pydantic import BaseModel
from business.tag import TagError
from teams.adaptive_card import Element


class ResourceCompliance(BaseModel):
    type: str
    id: str
    parent: Optional[str] = None
    errors: list[TagError]


class UserInfo(BaseModel):
    type: str
    primary: str
    secondary: Optional[str] = None


class ComplianceReport(BaseModel):
    region: str
    account: str
    user: UserInfo
    reports: list[ResourceCompliance]
