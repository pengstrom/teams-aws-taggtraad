from event.ec2 import CreateImageEvent
from business.compliance import *
from business.tag import AWSTag, Case
from error import *
from business import Tagger, TagConfig
from config import config


def mk_create_image_report(ev: CreateImageEvent) -> list[ResourceCompliance]:
    req = ev.requestParameters
    res = ev.responseElements

    image_tags: list[AWSTag] = []
    snapshot_tags: list[AWSTag] = []
    for ts in req.tagSpecificationSet.items:
        for t in ts.tags:
            tag = AWSTag(t.key, t.value)
            if ts.resourceType == "image":
                image_tags.append(tag)
            elif ts.resourceType == "snapshot":
                snapshot_tags.append(tag)
            else:
                raise UnexpectedTagResourceType(ts.resourceType)

    tagger = Tagger(TagConfig(config.req_keys, Case.CAPILATIZE, Case.LOWER))
    image_errors = tagger.validate(image_tags)
    snapshot_errors = tagger.validate(snapshot_tags)

    parent = f"{req.instanceId} ({req.name})"
    reports = []
    if len(image_errors) > 0:
        reports.append(
            ResourceCompliance(
                type="AMI", id=res.imageId, errors=image_errors, parent=parent
            )
        )
    if len(snapshot_errors) > 0:
        reports.append(
            ResourceCompliance(
                type="Snapshot", id="", errors=image_errors, parent=parent
            )
        )
    return reports
