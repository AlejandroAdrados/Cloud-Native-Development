from typing import Optional
import uuid
from enum import Enum


class State(Enum):
    CORRECT = "CORRECT"
    INCORRECT = "INCORRECT"
    UNSOLVED = "UNSOLVED"


class Type(Enum):
    ADDITION = "ADD"
    MULTIPLICATION = "MULT"
    DERIVATIVE = "DERIV"


class Assignment:
    """
    Assignment (=exercise) entity class.
    ---------
    Attribute:
        - state:   current state of the assignment.
        - type:    type of the assignment (e.g. multiplication, addition, ...)
        - content: list of numbers, which is used to
                   represent the content of an assignment.
        - id: id of assignment
    """

    def __init__(
        self,
        state: State,
        type: Type,
        content: list,
        id: Optional[uuid.UUID] = None,
    ):
        self.id = uuid.uuid4() if id is None else id
        self.state = state
        self.type = type
        self.content = content

    def get_dict(self):
        """
        Returns assignment as dictonary, which is needed for dynamodb objects.
        """
        assignment = {
            "Id": self.id,
            "State": self.state.value,
            "Type": self.type.value,
            "Content": self.content,
        }
        return assignment
