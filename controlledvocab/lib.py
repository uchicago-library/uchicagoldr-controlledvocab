from re import compile, IGNORECASE


class ControlledVocabulary(object):
    def __init__(self, contains=None, child_vocabs=None, patterns=None,
                 edit_before_build=False,
                 check_children=True, check_patterns=True,
                 case_sensitive=True):

        self.built_contains = None
        self.built_child_vocabs = None
        self.built_patterns = None

        self.check_children = check_children
        self.check_patterns = check_patterns
        self.case_sensitive = case_sensitive
        self.edit_before_build = edit_before_build

        self.set_contains(contains)
        self.set_child_vocabs(child_vocabs)
        self.set_patterns(patterns)

        if not edit_before_build:
            self.build_all()

    def __contains__(self, x):
        if self.built_contains is None or \
                self.built_child_vocabs is None or \
                self.built_patterns is None:
            raise AttributeError('Can not run without built sets.')
        if not isinstance(x, str):
            return False
        if self.case_sensitive:
            if x in self.built_contains:
                return True
        else:
            if x.lower() in self.built_contains:
                return True
        if self.check_children:
            for child_vocab in self.built_child_vocabs:
                if x in child_vocab:
                    return True
        if self.check_patterns:
            for pattern in self.built_patterns:
                if pattern.match(x):
                    return True
        return False

    def build_contains(self):
        if self.contains is None:
            self.built_contains = []
        else:
            if self.case_sensitive is False:
                self.built_contains = [x.lower() for x in self.contains]
            else:
                self.built_contains = self.contains

    def build_child_vocabs(self):
        if self.child_vocabs is None:
            self.built_child_vocabs = []
        else:
            self.built_child_vocabs = []
            for child_vocab in self.child_vocabs:
                self.built_child_vocabs.append(
                    child_vocab(check_children=self.check_children,
                                check_patterns=self.check_patterns,
                                case_sensitive=self.case_sensitive,
                                edit_before_build=self.edit_before_build)
                )

    def build_patterns(self):
        if self.patterns is None:
            self.built_patterns = []
        else:
            for pattern in self.patterns:
                if self.case_sensitive is False:
                    self.built_patterns.append(compile(pattern, IGNORECASE))
                else:
                    self.built_patterns.append(compile(pattern))

    def build_all(self):
        self.build_contains()
        self.build_child_vocabs()
        self.build_patterns()

    def set_contains(self, contains):
        self.contains = contains

    def get_contains(self):
        return self.contains

    def set_child_vocabs(self, child_vocabs):
        self.child_vocabs = child_vocabs

    def get_child_vocabs(self):
        return self.child_vocabs

    def set_patterns(self, patterns):
        self.patterns = patterns

    def get_patterns(self):
        return self.patterns


class ControlledVocabFromSource(object):
    def __init__(self, source):
        self.source = source
        self.contains = self.read_contains(self.source)
        self.child_vocabs = self.read_child_vocabs(self.source)
        self.patterns = self.read_patterns(self.source)
        self.edit_before_build = self.read_edit_before_build(self.source)
        self.check_children = self.read_check_children(self.source)
        self.check_patterns = self.read_check_patterns(self.source)
        self.case_sensitive = self.read_case_sensitive(self.source)

    def read_contains(source):
        raise NotImplemented

    def read_child_vocabs(source):
        raise NotImplemented

    def read_patterns(source):
        raise NotImplemented

    def read_edit_before_build(source):
        raise NotImplemented

    def read_check_children(source):
        raise NotImplemented

    def read_check_patterns(source):
        raise NotImplemented

    def read_case_sensitive(source):
        raise NotImplemented

    def build(self):
        return ControlledVocabulary(contains=self.contains,
                                    child_vocabs=self.child_vocabs,
                                    patterns=self.patterns,
                                    edit_before_build=self.edit_before_build,
                                    check_children=self.check_children,
                                    check_patterns=self.check_patterns,
                                    case_sensitive=self.case_sensitive)
