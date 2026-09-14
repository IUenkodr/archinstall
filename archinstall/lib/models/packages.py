from dataclasses import dataclass
from typing import Optional

@dataclass
class ThirdPartyRepository:
    name: str
    server: str
    gpg_key: Optional[str] = None

from dataclasses import dataclass
from typing import Optional

@dataclass
class Repository:
    name: str
    server: str

@dataclass
class ThirdPartyRepository(Repository):
    gpg_key: Optional[str] = None

