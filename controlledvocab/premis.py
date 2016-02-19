from controlledvocab.lib import ControlledVocabulary


class PremisVocabulary(ControlledVocabulary):
    def __init__(self, edit_before_build=False, check_children=True,
                 check_patterns=True, case_sensitive=True):

        contains = ['premis']
        child_vocabs = [ObjectVocabulary,
                        EventVocabulary,
                        RightsVocabulary,
                        AgentVocabulary]
        patterns = None

        ControlledVocabulary.__init__(self,
                                      contains=contains,
                                      child_vocabs=child_vocabs,
                                      patterns=patterns,
                                      edit_before_build=edit_before_build,
                                      check_children=check_children,
                                      check_patterns=check_patterns,
                                      case_sensitive=case_sensitive)


class EventVocabulary(ControlledVocabulary):
    def __init__(self, edit_before_build=False, check_children=True,
                 check_patterns=True, case_sensitive=True):

        contains = ['eventType',
                    'eventDateTime']
        child_vocabs = [EventIdentifierVocabulary,
                        EventDetailInformationVocabulary,
                        EventOutcomeInformationVocabulary,
                        LinkingAgentIdentifierVocabulary,
                        LinkingObjectIdentifierVocabulary]
        patterns = None

        ControlledVocabulary.__init__(self,
                                      contains=contains,
                                      child_vocabs=child_vocabs,
                                      patterns=patterns,
                                      edit_before_build=edit_before_build,
                                      check_children=check_children,
                                      check_patterns=check_patterns,
                                      case_sensitive=case_sensitive)


