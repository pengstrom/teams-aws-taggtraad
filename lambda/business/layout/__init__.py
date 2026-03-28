from aws_lambda_powertools import Logger
from enum import StrEnum, auto
from business.tag import *
from business.compliance import *
from event.cloudtrail import UserIdentity
from teams.adaptive_card import *
from event.envelope import *

logger = Logger()


# class AreaId(StrEnum):
#     RESOURCE_AREA = auto()
#     USER_AREA = auto()
#     ACTION_AREA = auto()
#     ERRORS_AREA = auto()


# class ElementId(StrEnum):
#     ACTION_ID = auto()
#     TOGGLE_ID = auto()
#     ERRORS_ID = auto()


# def mk_text_cell(text: str) -> TableCell:
#     return TableCell(items=[TextBlock(text=text)])


# def mk_error_row(key: str, value: str, error: str, msg: str) -> TableRow:
#     return TableRow(
#         cells=[
#             mk_text_cell(key),
#             mk_text_cell(value),
#             mk_text_cell(error),
#             mk_text_cell(msg),
#         ]
#     )


# def mk_layout(title: str, name: str, errors: list[TagError]):
#     areas = [
#         GridArea(name=AreaId.RESOURCE_AREA, row=1, column=1),
#         GridArea(name=AreaId.USER_AREA, row=1, column=2),
#         GridArea(name=AreaId.ACTION_AREA, row=2, columnSpan=2),
#         GridArea(name=AreaId.ERRORS_AREA, row=3, columnSpan=2),
#     ]
#     layout = LayoutAreaGrid(columns=[60], areas=areas)
#     titleBlock = TextBlock(
#         text=title, size=TextBlockSize.LARGE, weight=TextBlockWeight.BOLDER
#     )
#     resourceContainer = Container(
#         items=[titleBlock],
#         grid_area=AreaId.RESOURCE_AREA,  # pyright: ignore[reportCallIssue]
#     )  # pyright: ignore[reportCallIssue]
#     userBlock = TextBlock(
#         text=name, weight=TextBlockWeight.BOLDER, size=TextBlockSize.MEDIUM
#     )
#     userContainer = Container(
#         items=[userBlock],
#         grid_area=AreaId.USER_AREA,  # pyright: ignore[reportCallIssue]
#     )
#     toggleAction = ActionToggleVisibility(
#         id=ElementId.TOGGLE_ID,
#         title="Show Errors",
#         targetElements=[ElementId.ERRORS_ID],
#     )
#     actionSet = ActionSet(
#         id=ElementId.ACTION_ID,
#         grid_area=AreaId.ACTION_AREA,  # pyright: ignore[reportCallIssue]
#         actions=[toggleAction],
#     )
#     columns = [
#         TableColumn(width=1),
#         TableColumn(width=1),
#         TableColumn(width=2),
#         TableColumn(width=3),
#     ]
#     headerRow = TableRow(
#         cells=[
#             mk_text_cell("Key"),
#             mk_text_cell("Value"),
#             mk_text_cell("Error"),
#             mk_text_cell("Message"),
#         ]
#     )
#     rows = [headerRow]
#     for e in errors:
#         key = ""
#         value = ""
#         if e.kind == TagErrorKind.KEY_MISSING:
#             key = e.tags[0].Key
#         elif e.kind == TagErrorKind.KEY_CASE_INVALID:
#             key = e.tags[0].Key
#         elif e.kind == TagErrorKind.VALUE_CASE_INVALID:
#             value = e.tags[0].Value
#         elif e.kind == TagErrorKind.VALUE_NOT_ALLOWED:
#             value = e.tags[0].Value
#         rows.append(mk_error_row(key, value, e.kind, e.msg))
#     error_table = Table(firstRowAsHeaders=True, columns=columns, rows=rows)
#     error_container = Container(
#         id=ElementId.ERRORS_ID,
#         grid_area=AreaId.ERRORS_AREA,  # pyright: ignore[reportCallIssue]
#         items=[error_table],
#         isVisible=False,
#     )  # pyright: ignore[reportCallIssue]
#     elements = [resourceContainer, userContainer, actionSet, error_container]
#     card = AdaptiveCard(
#         body=elements, layouts=[layout]
#     )  # pyright: ignore[reportCallIssue]

#     return card


# def mk_assumed_role_layout(user: AssumedRoleUser) -> list[Element]:
#     elems: list[Element] = [TextBlock(text=user.type)]
#     principals = user.principalId.split(":")
#     if len(principals) > 0:
#         elems.append(TextBlock(text=principals[0]))
#         if len(principals) > 1:
#             elems.append(TextBlock(text=principals[1]))
#     else:
#         logger.warning(f"No info in principalId: {user.principalId}", user)
#     return elems


# def mk_generic_user_layout(user: UserIdentity) -> list[Element]:
#     return []


# def mk_user_layout(user: UserIdentity) -> Element:
#     items: list[Element] = [TextBlock(text=user.type)]
#     if user.type == UserType.ASSUMED_ROLE:
#         items = mk_assumed_role_layout(user)
#     else:
#         items = mk_generic_user_layout(user)
#     return Container(items=items)


def mk_text_cell(text: str) -> TableCell:
    return TableCell(items=[TextBlock(text=text)])


def mk_user_element(user: UserInfo) -> Container:
    header = TextBlock(
        text=user.primary, size=TextBlockSize.MEDIUM, weight=TextBlockWeight.BOLDER
    )
    subheading = f"{user.type}"
    if user.secondary:
        subheading = f"{subheading}: {user.secondary}"
    subheader = TextBlock(text=subheading)
    return Container(items=[header, subheader])


def mk_report_element(r: ResourceCompliance, index: int) -> Element:
    label = f"{r.type}: {r.id}"
    info = Container(
        grid_area="info",
        items=[
            TextBlock(text=label, weight=TextBlockWeight.BOLDER),
        ],
    )
    if r.parent:
        info.items.append(TextBlock(text=r.parent))

    show_id = f"show-{index}"
    hide_id = f"hide-{index}"
    errors_id = f"errors-{index}"
    targets = [errors_id]
    toggle = ActionSet(
        grid_area="toggle",
        actions=[
            ActionToggleVisibility(
                id=show_id, title="Show/Hide", targetElements=targets
            ),
        ],
    )

    rows = [
        TableRow(
            cells=[
                mk_text_cell("Error"),
                mk_text_cell("Key"),
                mk_text_cell("Value"),
                mk_text_cell("Message"),
            ]
        )
    ]
    for e in r.errors:
        key = ""
        value = ""
        if e.kind == TagErrorKind.KEY_MISSING:
            key = e.tags[0].Key
        elif e.kind == TagErrorKind.KEY_CASE_INVALID:
            key = e.tags[0].Key
        elif e.kind == TagErrorKind.VALUE_CASE_INVALID:
            value = e.tags[0].Value
        elif e.kind == TagErrorKind.VALUE_NOT_ALLOWED:
            key = e.tags[0].Key
            value = e.tags[0].Value

        rows.append(
            TableRow(
                cells=[
                    mk_text_cell(e.kind),
                    mk_text_cell(key),
                    mk_text_cell(value),
                    mk_text_cell(e.msg),
                ]
            )
        )
    errors = Table(
        id=errors_id,
        grid_area="errors",
        isVisible=False,
        firstRowAsHeaders=True,
        columns=[
            TableColumn(width=1),
            TableColumn(width=1),
            TableColumn(width=1),
            TableColumn(width=1),
        ],
        rows=rows,
    )

    areas: list[GridArea] = [
        GridArea(name="info", row=1, column=1),
        GridArea(name="toggle", row=1, column=2),
        GridArea(name="errors", row=2, columnSpan=2),
    ]
    return Container(
        showBorder=True,
        layouts=[LayoutAreaGrid(columns=[60], areas=areas)],
        items=[info, toggle, errors],
    )


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


# card = (user info, [resource info])
# resource info = ((resource type, resource id), errors toggle, [error])
def mk_teams_card(report: ComplianceReport) -> AdaptiveCard:
    account = ACCOUNTS.get(report.account, report.account)
    region = REGIONS.get(report.region, report.region)

    header = Container(
        grid_area="title",
        items=[
            TextBlock(
                text=account,
                size=TextBlockSize.LARGE,
                weight=TextBlockWeight.BOLDER,
            ),
            TextBlock(text=region),
        ],
    )

    user = mk_user_element(report.user)
    user.grid_area = "user"

    reports = Container(
        grid_area="resources",
        items=[mk_report_element(r, i) for i, r in enumerate(report.reports)],
    )

    areas = [
        GridArea(name="title", row=1, column=1),
        GridArea(name="user", row=1, column=2),
        GridArea(name="resources", row=2, columnSpan=2),
    ]
    layout = LayoutAreaGrid(columns=[50, 50], areas=areas)
    return AdaptiveCard(layouts=[layout], body=[header, user, reports])
