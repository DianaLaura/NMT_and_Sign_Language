import unittest

class Test_Align_sign_spoken_sentences_timestamps(unittest.TestCase):

    de = []
    sign = []
    timestamps = []
    line_lengths_sign = []
    line_lengths_timestamps = []

    def setUp(self):
        
        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Extracted_data_timestamps/full_set.de', 'r', encoding='utf8')
        self.de = infile.readlines()
        infile.close()
        
        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Extracted_data_timestamps/full_set.sign', 'r', encoding='utf8')
        self.sign = infile.readlines()
        infile.close()

        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Extracted_data_timestamps/full_set.time', 'r', encoding='utf8')
        self.timestamps = infile.readlines()
        infile.close()

        line_lengths_sign = []
        line_lengths_timestamps = []

        for i in range(0, len(self.sign)): 
            self.line_lengths_sign.append(len(self.sign[i].split()))
            self.line_lengths_timestamps.append(len(self.timestamps[i].split()))
    
    def test_FileLength(self):
        self.assertEqual(len(self.de), 52842)
    
    def test_AlignmentSignDe(self):
        self.assertEquals(len(self.de), len(self.sign))

    def test_AlignmentSignTimestamps(self):
        self.assertEquals(len(self.sign), len(self.timestamps))
    
    
    def test_TokenParallelity(self):
        self.assertSequenceEqual(self.line_lengths_sign, self.line_lengths_timestamps)

    
if __name__ == "__main__":
    unittest.main()


    