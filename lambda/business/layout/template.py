from jinja2 import PackageLoader, Environment, select_autoescape
import yaml as y
from teams.adaptive_card import AdaptiveCard
from business.compliance import ComplianceReport

env = Environment(
    loader=PackageLoader('business', 'layout'),
    autoescape=False,
)

def render_template(report: ComplianceReport) -> AdaptiveCard:
    tp = env.get_template('card.yml.j2')
    yml = tp.render(report.model_dump(by_alias=True, exclude_none=True, serialize_as_any=True))
    data = y.safe_load(yml)
    return AdaptiveCard.model_construct(data)