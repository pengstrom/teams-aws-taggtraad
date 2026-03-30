from aws_lambda_powertools.utilities.typing import LambdaContext
from event.envelope import EventBridgeEvent
from event.cloudtrail import UserIdentity
from config import cfg
from business.templates import render_error

class UnexpectedEventName(Exception):
    ev: EventBridgeEvent

    def __init__(self, ev: EventBridgeEvent):
        self.ev = ev
        super().__init__(
            f"No handler available for $.detail.eventType: {ev.detail.eventType}"
        )


class UnexpectedUserType(Exception):
    user_identity: UserIdentity

    def __init__(self, user_identity: UserIdentity):
        self.user_identity = user_identity
        super().__init__(
            f"No handler available for $.detail.userIdentity.type: {user_identity.type}"
        )


class UnexpectedTagResourceType(Exception):
    resource_type: str

    def __init__(
        self,
        resource_type: str,
    ):
        self.resource_type = resource_type
        super().__init__(
            f"No handler available for $.detail.eventType: {resource_type}"
        )


def handle_unexpected(e: Exception, ev: dict, ctx: LambdaContext):
    # teams error channel webhook
    card = render_error(e, ev, ctx)
    cfg.error_client.send(card) 
    pass
