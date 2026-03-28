from typing import Annotated, Optional

from pydantic import BaseModel, Field, ConfigDict
from enum import StrEnum


class Layout(BaseModel):
    type: str


class GridArea(BaseModel):
    name: str
    column: Optional[int] = None
    row: Optional[int] = None
    columnSpan: Optional[int] = None


class LayoutAreaGrid(Layout):
    type: str = "Layout.AreaGrid"
    columns: list[int]
    areas: list[GridArea]


class Element(BaseModel):
    id: Optional[str] = None
    showBorder: Optional[bool] = None
    type: str


class TextBlockStyle(StrEnum):
    DEFAULT = "default"
    COLUMN_HEADER = "columnHeader"
    HEADING = "heading"


class TextBlockSize(StrEnum):
    DEFAULT = "Default"
    EXTRA_LARGE = "ExtraLarge"
    MEDIUM = "Medium"
    LARGE = "Large"
    SMALL = "Small"


class TextBlockWeight(StrEnum):
    DEFAULT = "Default"
    BOLDER = "Bolder"
    LIGHTER = "Lighter"


class TextBlock(Element):
    type: str = "TextBlock"
    isVisible: bool = True
    style: Optional[TextBlockStyle] = TextBlockStyle.DEFAULT
    text: str
    size: Optional[TextBlockSize] = TextBlockSize.DEFAULT
    weight: Optional[TextBlockWeight] = TextBlockWeight.DEFAULT
    wrap: Optional[bool] = True


class Container(Element):
    model_config = ConfigDict(populate_by_name=True)

    layouts: Optional[list[Layout]] = None
    grid_area: Annotated[Optional[str], Field(default=None, alias="grid.area")] = None
    type: str = "Container"
    items: list[Element] = []


class TableColumn(BaseModel):
    width: int


class TableCell(BaseModel):
    type: str = "TableCell"
    items: list[Element] = []


class TableRow(BaseModel):
    type: str = "TableRow"
    cells: list[TableCell] = []


class Table(Element):
    model_config = ConfigDict(populate_by_name=True)

    type: str = "Table"
    isVisible: Optional[bool] = True
    firstRowAsHeaders: Optional[bool] = True
    grid_area: Annotated[Optional[str], Field(default=None, alias="grid.area")] = None
    columns: list[TableColumn] = []
    rows: list[TableRow] = []


class Action(BaseModel):
    type: str
    id: str
    isVisible: bool = True


class ActionToggleVisibility(Action):
    type: str = "Action.ToggleVisibility"
    title: str
    targetElements: list[str] = []


class ActionSet(Element):
    model_config = ConfigDict(populate_by_name=True)
    grid_area: Annotated[Optional[str], Field(default=None, alias="grid.area")] = None
    type: str = "ActionSet"
    actions: list[Action] = []


class TeamsCardProperties(BaseModel):
    width: Optional[str] = "full"


class AdaptiveCard(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    layouts: list[Layout] = []
    type: str = "AdaptiveCard"
    version: str = "1.5"
    msTeams: Optional[TeamsCardProperties] = TeamsCardProperties()
    schema_: str = Field(
        default="http://adaptivecards.io/schemas/adaptive-card.json", alias="$schema"
    )
    body: list[Element]


class AdaptiveCardItem(BaseModel):
    contentType: str = "application/vnd.microsoft.card.adaptive"
    contentUrl: None = None
    content: AdaptiveCard
