from re import match, compile

class ControlledVocabulary(object):
    def __init__(self, contains=None, child_vocabs=None, patterns=None):
        if contains is None:
            self.contains = []
        else:
            self.contains = contains
        if child_vocabs is None:
            self.child_vocabs = []
        else:
            for child_vocab in child_vocabs:
                self.child_vocabs.append(child_vocab())
        if patterns is None:
            self.patterns = []
        else:
            for pattern in patterns:
                self.patterns.append(compile(pattern))


    def __contains__(self, x):
        if x in self.contains:
            return True
        for child_vocab in self.child_vocabs:
            if x in child_vocab:
                return True
        for pattern in self.patterns:
            if pattern.match(x):
                return True
        return False
