from dataclasses import dataclass
from typing import List, Any, TypedDict


@dataclass
class ESConnectionSettings:
    hosts: List[str]


class CursorForGettingBatches(TypedDict):
    column_name: str
    value_to_start_from: Any