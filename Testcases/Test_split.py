import unittest


class Test_Align_sign_spoken_sentences(unittest.TestCase):

    train_de = []
    train_sign = []
    train_mouthings = []
    train_line_lengths_sign = []
    train_line_lengths_mouthings = []

    dev_de = []
    dev_sign = []
    dev_mouthings = []
    dev_line_lengths_sign = []
    dev_line_lengths_mouthings = []

    test_de = []
    test_sign = []
    test_mouthings = []
    test_line_lengths_sign = []
    test_line_lengths_mouthings = []

    def setUp(self):
        
        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Extracted_data/train.de', 'r', encoding='utf8')
        self.train_de = infile.readlines()
        infile.close()

        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Extracted_data/train.sign', 'r', encoding='utf8')
        self.train_sign = infile.readlines()
        infile.close()

        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Extracted_data/train.mouthings', 'r', encoding='utf8')
        self.train_mouthings = infile.readlines()
        infile.close()

        

        for i in range(0, len(self.train_sign)): 
            self.train_line_lengths_sign.append(len(self.train_sign[1].split()))
            self.train_line_lengths_mouthings.append(len(self.train_mouthings[1].split()))
    

        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Extracted_data/dev.de', 'r', encoding='utf8')
        self.dev_de = infile.readlines()
        infile.close()

        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Extracted_data/dev.sign', 'r', encoding='utf8')
        self.dev_sign = infile.readlines()
        infile.close()

        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Extracted_data/dev.mouthings', 'r', encoding='utf8')
        self.dev_mouthings = infile.readlines()
        infile.close()

        

        for i in range(0, len(self.dev_sign)): 
            self.dev_line_lengths_sign.append(len(self.dev_sign[1].split()))
            self.dev_line_lengths_mouthings.append(len(self.dev_mouthings[1].split()))
    
        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Extracted_data/test.de', 'r', encoding='utf8')
        self.test_de = infile.readlines()
        infile.close()

        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Extracted_data/test.sign', 'r', encoding='utf8')
        self.test_sign = infile.readlines()
        infile.close()

        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Extracted_data/test.mouthings', 'r', encoding='utf8')
        self.test_mouthings = infile.readlines()
        infile.close()

        

        for i in range(0, len(self.test_sign)): 
            self.test_line_lengths_sign.append(len(self.test_sign[1].split()))
            self.test_line_lengths_mouthings.append(len(self.test_mouthings[1].split()))
    
    def test_length_train_set(self):
        self.assertEquals(len(self.train_de), 48842)
        self.assertEquals(len(self.train_sign), 48842)
        self.assertEquals(len(self.train_mouthings), 48842)
    
    def test_token_parallelity_train(self):
        self.assertSequenceEqual(self.train_line_lengths_mouthings, self.train_line_lengths_sign)
    

    def test_length_dev_set(self):
        self.assertEquals(len(self.dev_de), 2000)
        self.assertEquals(len(self.dev_sign), 2000)
        self.assertEquals(len(self.dev_mouthings), 2000)
    
    def test_token_parallelity_dev(self):
        self.assertSequenceEqual(self.dev_line_lengths_mouthings, self.dev_line_lengths_sign)

    def test_length_test_set(self):
        self.assertEquals(len(self.test_de), 2000)
        self.assertEquals(len(self.test_sign), 2000)
        self.assertEquals(len(self.test_mouthings), 2000)
        
    def test_token_parallelity_test(self):
        self.assertSequenceEqual(self.test_line_lengths_mouthings, self.test_line_lengths_sign)


if __name__ == "__main__":
    unittest.main()