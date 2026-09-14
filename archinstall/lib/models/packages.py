from dataclasses import dataclass
from typing import Optional

@dataclass
class Repository:
    name: str
    server: str

@dataclass
class ThirdPartyRepository(Repository):
    gpg_key: Optional[str] = None

