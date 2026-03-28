from config import *
from event.cloudtrail import *
from event.envelope import EventBridgeEvent
from business.layout.template import render_template
from teams import Webhook
from teams.adaptive_card import *
from business.tag import *
from business.layout import *


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
                        f"Required tag key '{key}' missing!", [AWSTag(key, "")]
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
                        f"Tag value '{val}' not allowed! Only {valid_options} are allowed!",
                        [t],
                    )
                )

        return invalid

    def validate_case(self, tags: list[AWSTag]) -> list[TagError]:
        logger.debug("Tags %s", tags)
        wrongs: list[TagError] = []
        for t in tags:
            key = t.Key
            key_truth = normalize_case(key, self.cfg.key_case)
            if key != key_truth:
                wrongs.append(
                    mk_key_case_invalid(
                        f"Tag key '{key}' case incorrect! Should be '{key_truth}'!", [t]
                    )
                )
            value = t.Value
            value_truth = normalize_case(value, self.cfg.value_case)
            if value != value_truth:
                wrongs.append(
                    mk_value_case_invalid(
                        f"Tag value '{value}' case incorrect! Should be '{value_truth}'!",
                        [t],
                    )
                )
        return wrongs


# def mk_heading_element(title: str) -> TextBlock:
#     return TextBlock(text=title, style=TextBlockStyle.HEADING)


# def mk_error_element(err: TagError) -> TextBlock:
#     text = f"*ERROR: {err.kind}*: {err.msg}"
#     return TextBlock(text=text)


# def mk_report(
#     title: str, tags: list[AWSTag], errors: list[TagError]
# ) -> AdaptiveCardItem:
#     body: list[Element] = [mk_heading_element(title)]
#     for err in errors:
#         body.append(mk_error_element(err))
#     content = AdaptiveCard(body=body)  # pyright: ignore[reportCallIssue]
#     return AdaptiveCardItem(content=content)


# def get_tags(ev: AWSAPICallViaCloudTrail) -> list[AWSTag]:
#     tags: list[AWSTag] = []
#     for tssi in ev.requestParameters.tagSpecificationSet.items:
#         logger.debug("tssi", tssi)
#         for t in tssi.tags:
#             logger.debug("t", t)
#             tags.append(mk_aws_tag(t.key, t.value))
#     return tags


# def get_email(ev: AWSAPICallViaCloudTrail) -> str:
#     # parts = ev.userIdentity.principalId.split(":")
#     parts = ["abc", "a@b.c"]
#     return parts[len(parts) - 1]


# def get_title(ev: AWSAPICallViaCloudTrail) -> str:
#     name = ev.eventName
#     id = ev.responseElements.imageId
#     return f"{name}: {id}"


# def report_tag_errors(
#     webhook_url: str, ev: AWSAPICallViaCloudTrail, errors: list[TagError]
# ):
#     tags = get_tags(ev)
#     title = get_title(ev)
#     name = get_email(ev)
#     card = mk_layout(title, name, errors)
#     client = Webhook(webhook_url)
#     client.send(card)
#     return {"status": "reported", "errors": errors}


def mk_root_user(u: RootUser) -> UserInfo:
    return UserInfo(type="Root", primary=u.principalId, secondary=u.userName)


def mk_assumed_role_user(u: AssumedRoleUser) -> UserInfo:
    principals = u.principalId.split(":")
    primary = principals[1].strip()
    secondary = principals[0].strip()
    return UserInfo(type="IAM Identity Center", primary=primary, secondary=secondary)


def send_notification(ev: EventBridgeEvent, report: ComplianceReport):
    # card = mk_teams_card(report)
    card = render_template(report)

    client = Webhook(config.webhook_url)
    client.send(card)

    return RESULT_NOTIFIED
