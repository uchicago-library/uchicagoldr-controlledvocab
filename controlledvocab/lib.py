from re import compile, IGNORECASE
from json import load as jsonload


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
                if isinstance(child_vocab, ControlledVocabFromSource):
                        x = child_vocab.build(check_children=self.check_children,
                                          check_patterns=self.check_patterns,
                                          case_sensitive=self.case_sensitive,
                                          edit_before_build=self.edit_before_build)
                        self.built_child_vocabs.append(x)
                else:
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
            self.built_patterns = []
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
        self.set_source(source)

    def set_source(self, source):
        self.source = source

    def get_source(self):
        return self.source

    def read_contains(self, source=None):
        if source is None:
            source = self.source
        raise NotImplemented

    def read_child_vocabs(self, source=None):
        if source is None:
            source = self.source
        raise NotImplemented

    def read_patterns(self, source=None):
        if source is None:
            source = self.source
        raise NotImplemented

    def read_edit_before_build(self, source=None):
        if source is None:
            source = self.source
        raise NotImplemented

    def read_check_children(self, source=None):
        if source is None:
            source = self.source
        raise NotImplemented

    def read_check_patterns(self, source=None):
        if source is None:
            source = self.source
        raise NotImplemented

    def read_case_sensitive(self, source=None):
        if source is None:
            source = self.source
        raise NotImplemented

    def build(self, check_children=None, check_patterns=None,
              case_sensitive=None, edit_before_build=None):

        self.contains = self.read_contains()
        self.child_vocabs = self.read_child_vocabs()
        self.patterns = self.read_patterns()

        if edit_before_build is None:
            self.edit_before_build = self.read_edit_before_build()
        else:
            self.edit_before_build = edit_before_build

        if check_children is None:
            self.check_children = self.read_check_children()
        else:
            self.check_children = check_children

        if check_patterns is None:
            self.check_patterns = self.read_check_patterns()
        else:
            self.check_patterns = check_patterns

        if case_sensitive is None:
            self.case_sensitive = self.read_case_sensitive()
        else:
            self.case_sensitive = case_sensitive

        return ControlledVocabulary(contains=self.contains,
                                    child_vocabs=self.child_vocabs,
                                    patterns=self.patterns,
                                    edit_before_build=self.edit_before_build,
                                    check_children=self.check_children,
                                    check_patterns=self.check_patterns,
                                    case_sensitive=self.case_sensitive)


class ControlledVocabFromJson(ControlledVocabFromSource):
    def __init__(self, source):
        ControlledVocabFromSource.__init__(self, source)

    def read_contains(self, source=None):
        if source is None:
            source = self.source
        data = None
        with open(self.source, 'r') as f:
            data = jsonload(f)
        try:
            return data['contains']
        except KeyError:
            return []

    def read_child_vocabs(self, source=None):
        if source is None:
            source = self.source
        data = None
        with open(self.source, 'r') as f:
            data = jsonload(f)
        try:
            result = [ControlledVocabFromJson(x) for x in data['child_vocabs']]
            return result
        except KeyError:
            return []

    def read_patterns(self, source=None):
        if source is None:
            source = self.source
        data = None
        with open(self.source, 'r') as f:
            data = jsonload(f)
        try:
            return data['patterns']
        except KeyError:
            return []

    def read_edit_before_build(self, source=None):
        if source is None:
            source = self.source
        data = None
        with open(self.source, 'r') as f:
            data = jsonload(f)
        try:
            x = data['edit_before_build']
            if x == 'True':
                return True
            if x == 'False':
                return False
        except KeyError:
            return False

    def read_check_children(self, source=None):
        if source is None:
            source = self.source
        data = None
        with open(self.source, 'r') as f:
            data = jsonload(f)
        try:
            x = data['check_children']
            if x == 'True':
                return True
            if x == 'False':
                return False
        except KeyError:
            return True

    def read_check_patterns(self, source=None):
        if source is None:
            source = self.source
        data = None
        with open(self.source, 'r') as f:
            data = jsonload(f)
        try:
            x = data['check_patterns']
            if x == 'True':
                return True
            if x == 'False':
                return False
        except KeyError:
            return True

    def read_case_sensitive(self, source=None):
        if source is None:
            source = self.source
        data = None
        with open(self.source, 'r') as f:
            data = jsonload(f)
        try:
            x = data['case_sensitive']
            if x == 'True':
                return True
            if x == 'False':
                return False
        except KeyError:
            return False
