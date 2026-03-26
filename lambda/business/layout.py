from aws_lambda_powertools import Logger

from adaptive_card import *
from enum import StrEnum, auto

from aws.event_bridge import *
from .tag import TagError, TagErrorKind

logger = Logger()


class AreaId(StrEnum):
    RESOURCE_AREA = auto()
    USER_AREA = auto()
    ACTION_AREA = auto()
    ERRORS_AREA = auto()


class ElementId(StrEnum):
    ACTION_ID = auto()
    TOGGLE_ID = auto()
    ERRORS_ID = auto()


def mk_text_cell(text: str) -> TableCell:
    return TableCell(items=[TextBlock(text=text)])


def mk_error_row(key: str, value: str, error: str, msg: str) -> TableRow:
    return TableRow(
        cells=[
            mk_text_cell(key),
            mk_text_cell(value),
            mk_text_cell(error),
            mk_text_cell(msg),
        ]
    )


def mk_layout(title: str, name: str, errors: list[TagError]):
    areas = [
        GridArea(name=AreaId.RESOURCE_AREA, row=1, column=1),
        GridArea(name=AreaId.USER_AREA, row=1, column=2),
        GridArea(name=AreaId.ACTION_AREA, row=2, columnSpan=2),
        GridArea(name=AreaId.ERRORS_AREA, row=3, columnSpan=2),
    ]
    layout = LayoutAreaGrid(columns=[60], areas=areas)
    titleBlock = TextBlock(
        text=title, size=TextBlockSize.LARGE, weight=TextBlockWeight.BOLDER
    )
    resourceContainer = Container(
        items=[titleBlock],
        grid_area=AreaId.RESOURCE_AREA,  # pyright: ignore[reportCallIssue]
    )  # pyright: ignore[reportCallIssue]
    userBlock = TextBlock(
        text=name, weight=TextBlockWeight.BOLDER, size=TextBlockSize.MEDIUM
    )
    userContainer = Container(
        items=[userBlock],
        grid_area=AreaId.USER_AREA,  # pyright: ignore[reportCallIssue]
    )
    toggleAction = ActionToggleVisibility(
        id=ElementId.TOGGLE_ID,
        title="Show Errors",
        targetElements=[ElementId.ERRORS_ID],
    )
    actionSet = ActionSet(
        id=ElementId.ACTION_ID,
        grid_area=AreaId.ACTION_AREA,  # pyright: ignore[reportCallIssue]
        actions=[toggleAction],
    )
    columns = [
        TableColumn(width=1),
        TableColumn(width=1),
        TableColumn(width=2),
        TableColumn(width=3),
    ]
    headerRow = TableRow(
        cells=[
            mk_text_cell("Key"),
            mk_text_cell("Value"),
            mk_text_cell("Error"),
            mk_text_cell("Message"),
        ]
    )
    rows = [headerRow]
    for e in errors:
        key = ""
        value = ""
        if e.kind == TagErrorKind.KEY_MISSING:
            key = e.tags[0].Key
        elif e.kind == TagErrorKind.KEY_CASE_INVALID:
            key = e.tags[0].Key
        elif e.kind == TagErrorKind.VALUE_CASE_INVALID:
            value = e.tags[0].Value
        elif e.kind == TagErrorKind.KEY_CASE_INVALID:
            value = e.tags[0].Value
        rows.append(mk_error_row(key, value, e.kind, e.msg))
    error_table = Table(firstRowAsHeaders=True, columns=columns, rows=rows)
    error_container = Container(
        id=ElementId.ERRORS_ID,
        grid_area=AreaId.ERRORS_AREA,  # pyright: ignore[reportCallIssue]
        items=[error_table],
        isVisible=False,
    )  # pyright: ignore[reportCallIssue]
    elements = [resourceContainer, userContainer, actionSet, error_container]
    card = AdaptiveCard(
        body=elements, layouts=[layout]
    )  # pyright: ignore[reportCallIssue]

    print(card)
    return card


def mk_assumed_role_layout(user: AssumedRoleUser) -> list[Element]:
    elems: list[Element] = [TextBlock(text=user.type)]
    principals = user.principalId.split(":")
    if len(principals) > 0:
        elems.append(TextBlock(text=principals[0]))
        if len(principals) > 1:
            elems.append(TextBlock(text=principals[1]))
    else:
        logger.warning(f"No info in principalId: {user.principalId}", user)
    return elems


def mk_generic_user_layout(user: UserIdentity) -> list[Element]:
    return []


def mk_user_layout(user: UserIdentity) -> Element:
    items: list[Element] = [TextBlock(text=user.type)]
    if user.type == UserType.ASSUMED_ROLE:
        items = mk_assumed_role_layout(user)
    else:
        items = mk_generic_user_layout(user)
    return Container(items=items)
