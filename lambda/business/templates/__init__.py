import json
from aws_lambda_powertools.utilities.typing import LambdaContext
from jinja2 import PackageLoader, Environment, select_autoescape
import yaml as y
from teams.adaptive_card import AdaptiveCard
from business.compliance import ComplianceReport

ACCOUNTS = {
    "255300924049": "SLI",
    "952457084211": "nWise AB",
    "654654584681": "nWise Testing",
}

REGIONS = {
    "eu-north-1": "Stockholm",
    "eu-central-1": "Frankfurt",
    "eu-central-2": "Zurich",
    "eu-west-1": "Ireland",
    "eu-west-2": "London",
}

env = Environment(
    loader=PackageLoader('business', 'templates'),
    autoescape=False,
)

def render_template(original: dict, report: ComplianceReport) -> AdaptiveCard:
    dp = report.model_dump(by_alias=True, exclude_none=True, serialize_as_any=True)
    ev = json.dumps(original, indent=2)

    tp = env.get_template('card.yml.j2')
    yml = tp.render(**dp, original=ev)
    data = y.safe_load(yml)

    card = AdaptiveCard.model_construct(**data)
    return card

def render_error(error: Exception, event: dict, ctx: LambdaContext) -> AdaptiveCard:
    event_j = json.dumps(event, indent=2)
    ctx_j = json.dumps(ctx.__dict__, indent=2)
    err_j = str(error)
    
    tp = env.get_template('error.yml.j2')
    yml = tp.render(error=err_j, event=event_j, ctx=ctx_j)
    data: dict = y.safe_load(yml)

    card = AdaptiveCard.model_validate(data, by_alias=True)
    # print(card.model_dump_json(by_alias=True, exclude_none=True, serialize_as_any=True))
    return card