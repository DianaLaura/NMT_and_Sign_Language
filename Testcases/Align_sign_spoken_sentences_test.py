import unittest


class Test_Align_sign_spoken_sentences(unittest.TestCase):
    de = []
    sign = []
    mouthings = []
    line_lengths_sign = []
    line_lengths_mouthings = []

    def setUp(self):
        
        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Extracted_data/full_set.de', 'r', encoding='utf8')
        self.de = infile.readlines()
        infile.close()
        
        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Extracted_data/full_set.sign', 'r', encoding='utf8')
        self.sign = infile.readlines()
        infile.close()

        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Extracted_data/full_set.mouthings', 'r', encoding='utf8')
        self.mouthings = infile.readlines()
        infile.close()

        line_lengths_sign = []
        line_lengths_mouthings = []

        for i in range(0, len(self.sign)): 
            self.line_lengths_sign.append(len(self.sign[i].split()))
            self.line_lengths_mouthings.append(len(self.mouthings[i].split()))
            


    
    def test_FileLength(self):
        self.assertEqual(len(self.de), 52842)
    
    def test_AlignmentSignDe(self):
        self.assertEquals(len(self.de), len(self.sign))

    def test_AlignmentSignMouthings(self):
        self.assertEquals(len(self.sign), len(self.mouthings))
    
    
    def test_TokenParallelity(self):
        self.assertSequenceEqual(self.line_lengths_sign, self.line_lengths_mouthings)

    
if __name__ == "__main__":
    unittest.main()


        