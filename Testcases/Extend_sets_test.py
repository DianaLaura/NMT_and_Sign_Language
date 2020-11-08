import unittest

class Test_Extend_sets(unittest.TestCase):
    dev_sign_old = []
    dev_sign_new = []
    dev_mouthings = []
    dev_de_new = []
    dev_de_old = []

    test_sign_old = []
    test_sign_new = []
    test_mouthings = []
    test_de_new = []
    test_de_old = []


    train_de_old = []
    train_de_new = []
    line_lengths_sign = []
    line_lengths_mouthings = []


    def setUp(self):
        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Train_Test_Devsets/dev.sign', 'r', encoding='utf8')
        self.dev_sign_old = infile.readlines()
        infile.close()

        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Train_Test_Devsets/dev.de', 'r', encoding='utf8')
        self.dev_de_old = infile.readlines()
        infile.close()

        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Train_Test_Devsets/test.sign', 'r', encoding='utf8')
        self.test_sign_old = infile.readlines()
        infile.close()

        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Train_Test_Devsets/test.de', 'r', encoding='utf8')
        self.test_de_old = infile.readlines()
        infile.close()

        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Train_Test_Devsets/train.de', 'r', encoding='utf8')
        self.train_de_old = infile.readlines()
        infile.close()

        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Extracted_data/train.de', 'r', encoding='utf8')
        self.train_de_new = infile.readlines()
        infile.close()



        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Extracted_data/dev.sign', 'r', encoding='utf8')
        self.dev_sign_new = infile.readlines()
        infile.close()

        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Extracted_data/dev.de', 'r', encoding='utf8')
        self.dev_de_new = infile.readlines()
        infile.close()
    
        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Extracted_data/dev.mouthings', 'r', encoding='utf8')
        self.dev_mouthings = infile.readlines()
        infile.close()



        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Extracted_data/test.sign', 'r', encoding='utf8')
        self.test_sign_new = infile.readlines()
        infile.close()

        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Extracted_data/test.de', 'r', encoding='utf8')
        self.test_de_new = infile.readlines()
        infile.close()
    
        infile = open ('/Users/dianaenggist/Documents/NT_sign_language/Extracted_data/test.mouthings', 'r', encoding='utf8')
        self.test_mouthings = infile.readlines()
        infile.close()

        for i in range(0, len(self.dev_sign_new)): 
            self.line_lengths_sign.append(len(self.dev_sign_new[1].split()))
            self.line_lengths_mouthings.append(len(self.dev_mouthings[1].split()))

    def test_length_devset_mouthings(self):
        self.assertEquals(len(self.dev_mouthings), 2000)
    
    def test_length_devset_sign(self):
        self.assertEquals(len(self.dev_sign_new), 2000)
    
    def test_new_devset_parallel_to_old_devset(self):
        self.assertSequenceEqual(self.dev_de_old, self.dev_de_new)

    def test_new_devset_sign_parallel_to_old_devset(self):
        self.assertSequenceEqual(self.dev_sign_old, self.dev_sign_new)

    def test_length_testset_mouthings(self):
        self.assertEquals(len(self.test_mouthings), 2000)
    
    def test_length_testset_sign(self):
        self.assertEquals(len(self.test_sign_new), 2000)
    
    def test_new_testset_parallel_to_old_testset(self):
        self.assertSequenceEqual(self.test_de_old, self.test_de_new)

    def test_new_testset_sign_parallel_to_old_testset(self):
        self.assertSequenceEqual(self.test_sign_old, self.test_sign_new)
    
    def test_length_train_set(self):
        self.assertEquals(len(self.train_de_new), 48842)
    
    def test_TokenParallelity(self):
        self.assertSequenceEqual(self.line_lengths_sign, self.line_lengths_mouthings)

if __name__ == "__main__":
    unittest.main()