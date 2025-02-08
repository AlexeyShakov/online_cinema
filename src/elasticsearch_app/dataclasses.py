from dataclasses import dataclass
from typing import List


@dataclass
class ESConnectionSettings:
    hosts: List[str]
