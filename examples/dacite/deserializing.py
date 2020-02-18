from dataclasses import dataclass

from dacite import Config
from dacite import from_dict

from dep.base import Dependent
from dep.numeric import Natural


@dataclass(frozen=True)
class Book:
    id: Natural


config = Config(cast=[Dependent])
instance = from_dict(Book, {"id": 1}, config=config)
# reveal_type(instance.id) # N: Revealed type is 'dep.numeric.Natural'

# raises ValueError: Can't create Natural from -1
from_dict(Book, {"id": -1}, config=config)
