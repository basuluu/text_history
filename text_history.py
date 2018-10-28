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
    
    def check_for_ValueError(self, text, pos, length=None):
        if pos == None:
            pos = len(self._text)
        if isinstance(pos,int) and not pos < 0 and pos <= len(self._text):
            self._pos = pos
            if length and len(self._text[pos:]) < length:
                raise ValueError
            return pos
        raise ValueError
                
    def insert(self, text, pos=None):
        pos = self.check_for_ValueError(text, pos)
        action = InsertAction(pos, text, from_version = self._version, to_version = self._version + 1)
        return self.action(action)

    def replace(self, text, pos=None):
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

    def optimus(self, act, action):
        if isinstance(action, DeleteAction) and isinstance(act, DeleteAction):
            if action.pos in range(act.pos, act.length + 1):
                act.length = act.length + action.length
                act.pos = min(act.pos, action.pos)
            else:
                self.action_to_return.append(act)
                act = action
                return act
        elif isinstance(action,InsertAction) and isinstance(act, InsertAction):
            if action.pos in range(act.pos, act.pos + len(act.text) + 1):
                act.text = act.text[:action.pos] + action.text + act.text[action.pos:]
            else:
                self.action_to_return.append(act)
                act = action
                return act
        elif isinstance(action, ReplaceAction):
            if act != None:
                self.action_to_return.append(act)
            self.action_to_return.append(action)
            act = None 
            return act
        else:
            if act != None:
                self.action_to_return.append(act)
            act = action

        return act

    def get_actions(self, from_version=0, to_version=None):
        if to_version == None:
            to_version = self._version
        if from_version < 0 or from_version > to_version or to_version > self._version:
            raise ValueError
        else:
            self.action_to_return = []
            act = None
            for action in self._actions:
                if not action.from_version < from_version and not action.to_version > to_version:
                   act = self.optimus(act, action)
                elif action.to_version > to_version:
                   break
            if act != None:
                self.action_to_return.append(act)
            return self.action_to_return


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

    def __repr__(self):
        return "InsertAction(pos = {!r}, text = {!r}, v1 = {!r}, v2 = {!r})".format(self.pos, self.text, self.from_version, self.to_version) 


class ReplaceAction(Action):
    def apply(self, str):
        str = str[:self.pos] + self.text + str[self.pos + len(self.text):]
        return str
   
    def __repr__(self):
        return "ReplaceAction(pos = {!r}, text = {!r}, v1 = {!r}, v2 = {!r})".format(self.pos, self.text, self.from_version, self.to_version) 
  
      
class DeleteAction(Action):
    def __init__(self, pos, length, from_version, to_version):
        self.length = length
        self.pos = pos
        self.from_version = from_version
        self.to_version = to_version

    def apply(self, str):
        str = str[:self.pos] + str[self.pos + self.length:]
        return str

    def __repr__(self):
        return "DeleteAction(pos = {!r}, length = {!r}, v1 = {!r}, v2 = {!r})".format(self.pos, self.length, self.from_version, self.to_version)

