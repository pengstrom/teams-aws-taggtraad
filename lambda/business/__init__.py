from logger import logger
from config import cfg, RESULT_NO_ACTION, RESULT_NOTIFIED
from event.cloudtrail import *
from event.envelope import EventBridgeEvent
from business.templates import render_template
from teams import Webhook
from teams.adaptive_card import *
from model import *
from business.templates import *
from business.compliance import *


class Tagger:
    cfg: TagConfig

    def __init__(self, cfg: TagConfig):
        self.cfg = cfg

    def validate(self, tags: list[AWSTag]) -> list[TagError]:
        errors: list[TagError] = []

        errors.extend(self.validate_required_keys(tags))
        errors.extend(self.validate_allowed_values(tags))
        errors.extend(self.validate_case(tags))

        return errors

    def validate_required_keys(self, tags: list[AWSTag]) -> list[TagError]:
        missing: list[TagError] = []
        tag_keys = [t.Key for t in tags]
        for key in self.cfg.required_keys:
            if key not in tag_keys:
                missing.append(
                    mk_key_missing(
                        f"Required tag key **{key}** missing!", AWSTag(key, "")
                    )
                )

        return missing

    def validate_allowed_values(self, tags: list[AWSTag]) -> list[TagError]:
        invalid: list[TagError] = []
        for t in tags:
            valids = self.cfg.valid_values.get(t.Key)
            if not valids:
                continue
            valid_options = [v.lower() for v in valids]
            val = t.Value.lower()
            if t.Value.lower() not in valid_options:
                invalid.append(
                    mk_value_not_allowed(
                        f"Tag value **{val}** not allowed! Only **{valid_options}** are allowed!",
                        t,
                    )
                )

        return invalid

    def validate_case(self, tags: list[AWSTag]) -> list[TagError]:
        wrongs: list[TagError] = []
        for t in tags:
            key = t.Key
            key_truth = normalize_case(key, self.cfg.key_case)
            if key != key_truth:
                wrongs.append(
                    mk_key_case_invalid(
                        f"Tag key **{key}** case incorrect! Should be **{key_truth}**!", t
                    )
                )
            value = t.Value
            value_truth = normalize_case(value, self.cfg.value_case)
            if value != value_truth:
                wrongs.append(
                    mk_value_case_invalid(
                        f"Tag value **{value}** case incorrect! Should be **{value_truth}**!",
                        t,
                    )
                )
        return wrongs


def mk_root_user(u: RootUser) -> UserInfo:
    return UserInfo(type="Root", primary=u.principalId, secondary=u.userName)


def mk_assumed_role_user(u: AssumedRoleUser) -> UserInfo:
    principals = u.principalId.split(":")
    primary = principals[1].strip()
    secondary = principals[0].strip()
    return UserInfo(type="IAM Identity Center", primary=primary, secondary=secondary)


def send_notification(original: dict, ev: EventBridgeEvent, report: ComplianceReport):
    card = render_template(original, report)
    cfg.notify_client.send(card)

    return RESULT_NOTIFIED
