class TextHistory:
    def __init__(self):
        self._text = ''
        self._version = 0
        self._actions = []
        self._pos = len(self._text)

    @property
    def text(self):
        return self._text

    @property
    def version(self):
        return self._version
    
    def check_for_ValueError(self, text, pos, length = None):
        if pos == None:
            pos = len(self._text)
        if type(pos) == int and not pos < 0 and pos <= len(self._text):
            self._pos = pos
            if length and len(self._text[pos:]) < length:
                raise ValueError
            return pos
        raise ValueError
                
    def insert(self, text, pos = None):
        pos = self.check_for_ValueError(text, pos)
        action = InsertAction(pos, text, from_version = self._version, to_version = self._version + 1)
        return self.action(action)

    def replace(self, text, pos = None):
        pos = self.check_for_ValueError(text, pos)
        action = ReplaceAction(pos, text, from_version = self._version, to_version = self._version + 1)
        return self.action(action)
    
    def delete(self, pos, length):
        pos = self.check_for_ValueError(self._text, pos, length)
        action = DeleteAction(pos, length,  from_version = self._version, to_version = self._version + 1)
        return self.action(action)

    def action(self, action):
        self._actions.append(action)
        action.version_check()
        self._text = action.apply(self._text)
        self._version = action.to_version
        return self._version

    def get_actions(self, from_version = 0, to_version = None):
        if to_version == None:
            to_version = self._version
        if from_version < 0 or from_version > to_version or to_version > self._version:
            raise ValueError
        else:
            action_to_return = []
            for action in self._actions:
                if not action.from_version < from_version and not action.from_version > to_version and to_version != 0:
                    action_to_return.append(action)
            return action_to_return

class Action:
    def __init__(self, pos, text, from_version, to_version):
        self.text = text
        self.pos = pos
        self.from_version = from_version
        self.to_version = to_version

    def version_check(self):
        if not (self.from_version < self.to_version):
            raise ValueError

class InsertAction(Action):
    def apply(self, str):
        str = str[:self.pos] + self.text + str[self.pos:]
        return str


class ReplaceAction(Action):
    def apply(self, str):
        str = str[:self.pos] + self.text + str[self.pos + len(self.text):]
        return str
        
class DeleteAction(Action):
    def __init__(self, pos, length, from_version, to_version):
        self.length = length
        self.pos = pos
        self.from_version = from_version
        self.to_version = to_version

    def apply(self, str):
        str = str[:self.pos] + str[self.pos + self.length:]
        return str
