import unittest
from os import getcwd
from os.path import join

from controlledvocab.lib import ControlledVocabulary, ControlledVocabFromJson

class Test(unittest.TestCase):
    def test(self):
        cv = ControlledVocabFromJson(join(getcwd(),'testvocab1.json')).build()
        self.assertTrue('this' in cv)
        self.assertTrue('testvocabterm' in cv)
        self.assertTrue('that' in cv)
        self.assertTrue('thenext' in cv)
        self.assertTrue('thing' in cv)

if __name__ == '__main__':
    unittest.main()
