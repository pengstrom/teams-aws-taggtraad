from aws_lambda_powertools.logging import Logger
from error import *
from event.cloudtrail import *
from event.envelope import *
from business import *
from business.compliance import *
from business.ec2.create_image import mk_create_image_report

logger = Logger()


def dispatch(ev: EventBridgeEvent) -> ComplianceReport:
    d = ev.detail

    user: UserInfo | None = None
    if d.userIdentity.type == UserType.ROOT:
        logger.debug("Root user %s", d.userIdentity)
        user = mk_root_user(d.userIdentity)
        pass
    if d.userIdentity.type == UserType.IAM_USER:
        logger.debug("IAM user %s", d.userIdentity)
        pass
    if d.userIdentity.type == UserType.ASSUMED_ROLE:
        logger.debug("Assumed Role user %s", d.userIdentity)
        user = mk_assumed_role_user(d.userIdentity)
        pass
    if d.userIdentity.type == UserType.ROLE:
        logger.debug("Role user %s", d.userIdentity)
        pass

    if not user:
        raise UnexpectedUserType(d.userIdentity)

    reports: list[ResourceCompliance] = []
    if d.eventName == "CreateImage":
        logger.debug("CreateImage %s", ev.detail)
        reports = mk_create_image_report(d)
    elif d.eventName == "RunInstance":
        pass
    #     logger.debug("RunInstance", ev.detail)
    #     return mk_run_instance_report(d)
    else:
        raise UnexpectedEventName(ev)

    return ComplianceReport(
        user=user, reports=reports, region=d.awsRegion, account=d.recipientAccountId
    )
