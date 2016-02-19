from controlledvocabulary.lib import ControlledVocabulary

class PremisVocabulary(ControlledVocabulary):
    def __init__(self):
        ControlledVocabulary.__init__(self, child_vocabs=[ObjectVocabulary, EventVocabulary, RightsVocabulary, AgentVocabulary])
