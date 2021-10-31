
from core import Action

from enum import Enum


class FarononaActionType(Enum):

    MOVE = 1

class FarononaAction(Action):

    def __init__(self, action_type, win_by='APPROACH', **kwargs):
        """This is the format that every action must have. Dependending of the action type additional parameters can be asked.
            Example : a move from (0, 1) to (0, 2) is equivalent to FarononaAction(action_type=FarononaActionType.MOVE, at=(0, 1), to=(0, 2))

        Args:
            action_type (FarononaActionType): The type of the performed action.
        """
        assert isinstance(action_type, FarononaActionType), "Not a good action type format"
        self.action_type = action_type

        if action_type == FarononaActionType.MOVE:
            assert ((len(kwargs) == 2) and ('to' in kwargs.keys()) and ('at' in kwargs.keys())),\
                "Need you to add argument 'at' and 'to'"
            assert isinstance(kwargs['to'], tuple) and isinstance(kwargs['at'], tuple),\
                "to and from has to be a tuple"

        self.action = kwargs 
        self.win_by = win_by

    def __repr__(self):
        return str(self.get_action_as_dict())

    def get_action_as_dict(self):
        return {'action_type': self.action_type,
                'action': self.action,
                'winby': self.win_by}

    def get_json_action(self):
        return {'action_type': self.action_type.name,
                'action': self.action}

    def get_action(self):
        return self.action_type.name
