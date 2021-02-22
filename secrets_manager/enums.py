from enum import Enum
from typing import Any, Set


class BaseEnum(Enum):
    """
    Base Enum with methods that all of our enums should implement
    """
    @classmethod
    def has_value(cls, value: Any) -> bool:
        """
        Return true / false for whether the input is stored as a value in the enum
        """
        values = NLPType.get_values()
        return value in values

    @classmethod
    def get_values(cls) -> Set[Any]:
        """
        Return a list of the values stored within the enum
        """
        return set(item.value for item in cls)

class UserType(BaseEnum):
    """
    Store user type, returning or new user
    """
    returning_user = 'returning_user'
    new_user = 'new_user'