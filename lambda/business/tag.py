from dataclasses import dataclass

from pydantic import BaseModel
from enum import StrEnum, auto


@dataclass
class AWSTag:
    Key: str
    Value: str

    def __eq__(self, other):
        return self.Key == other.Key and self.Value == other.Value


def mk_aws_tag(key: str, value: str) -> AWSTag:
    return AWSTag(Key=key, Value=value)


class Case(StrEnum):
    UPPER = "UPPER"
    LOWER = "LOWER"
    CAPILATIZE = "CAPITALIZE"


def normalize_case(s: str, case: Case):
    if case is Case.UPPER:
        return s.upper()
    elif case is Case.LOWER:
        return s.lower()
    elif case is Case.CAPILATIZE:
        return s.capitalize()
    else:
        raise Exception(
            f"Unrecognized Case: '{case}'! Expected one of {[Case.UPPER, Case.LOWER, Case.CAPILATIZE]}!"
        )


class TagConfig:
    required_keys: list[str]
    valid_values: dict[str, list[str]]
    key_case: Case
    value_case: Case

    def __init__(self, req_keys, key_case, value_case):
        self.required_keys = req_keys
        self.key_case = key_case
        self.value_case = value_case
        self.valid_values = {}

    def set_valid_values(self, key: str, values: list[str]):
        self.valid_values[key] = values


class TagErrorKind(StrEnum):
    KEY_MISSING = "KEY_MISSING"
    KEY_CASE_INVALID = "KEY_CASE_INVALID"
    VALUE_CASE_INVALID = "VALUE_CASE_INVALID"
    VALUE_NOT_ALLOWED = "VALUE_NOT_ALLOWED"


class TagError(BaseModel):
    kind: TagErrorKind
    msg: str
    tags: list[AWSTag]


def mk_key_missing(msg: str, tags: list[AWSTag]):
    return TagError(kind=TagErrorKind.KEY_MISSING, msg=msg, tags=tags)


def mk_key_case_invalid(msg: str, tags: list[AWSTag]):
    return TagError(kind=TagErrorKind.KEY_CASE_INVALID, msg=msg, tags=tags)


def mk_value_case_invalid(msg: str, tags: list[AWSTag]):
    return TagError(kind=TagErrorKind.VALUE_CASE_INVALID, msg=msg, tags=tags)


def mk_value_not_allowed(msg: str, tags: list[AWSTag]):
    return TagError(kind=TagErrorKind.VALUE_NOT_ALLOWED, msg=msg, tags=tags)
