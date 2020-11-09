import unittest

class Test_Extend_sets_timestamps(unittest.TestCase):
    dev_sign_old = []
    dev_sign_new = []
    dev_timestamps = []
    dev_de_new = []
    dev_de_old = []

    test_sign_old = []
    test_sign_new = []
    test_timestamps = []
    test_de_new = []
    test_de_old = []


    train_de_old = []
    train_de_new = []
    line_lengths_sign = []
    line_lengths_timestamps = []


    def setUp(self): 

        infile = open ('/Your_path_to_original_sets_here/dev.de', 'r', encoding='utf8')
        self.dev_de_old = infile.readlines()
        infile.close()

        infile = open ('/Your_path_to_original_sets_here/test.sign', 'r', encoding='utf8')
        self.test_sign_old = infile.readlines()
        infile.close()

        infile = open ('/Your_path_to_original_sets_here/test.de', 'r', encoding='utf8')
        self.test_de_old = infile.readlines()
        infile.close()

        infile = open ('/Your_path_to_original_sets_here/train.de', 'r', encoding='utf8')
        self.train_de_old = infile.readlines()
        infile.close()

        infile = open ('/Your_Path_to_new_sets_here/train.de', 'r', encoding='utf8')
        self.train_de_new = infile.readlines()
        infile.close()



        infile = open ('/Your_Path_to_new_sets_here/dev.sign', 'r', encoding='utf8')
        self.dev_sign_new = infile.readlines()
        infile.close()

        infile = open ('/Your_Path_to_new_sets_here/dev.de', 'r', encoding='utf8')
        self.dev_de_new = infile.readlines()
        infile.close()
    
        infile = open ('/Your_Path_to_new_sets_here/dev.time', 'r', encoding='utf8')
        self.dev_timestamps = infile.readlines()
        infile.close()



        infile = open ('/Your_Path_to_new_sets_here/test.sign', 'r', encoding='utf8')
        self.test_sign_new = infile.readlines()
        infile.close()

        infile = open ('/Your_Path_to_new_sets_here/test.de', 'r', encoding='utf8')
        self.test_de_new = infile.readlines()
        infile.close()
    
        infile = open ('/Your_Path_to_new_sets_here/test.time', 'r', encoding='utf8')
        self.test_timestamps = infile.readlines()
        infile.close()

        for i in range(0, len(self.dev_sign_new)): 
            self.line_lengths_sign.append(len(self.dev_sign_new[i].split()))
            self.line_lengths_timestamps.append(len(self.dev_timestamps[i].split()))

    def test_length_devset_timestamps(self):
        self.assertEquals(len(self.dev_timestamps), 2000)
    
    def test_length_devset_sign(self):
        self.assertEquals(len(self.dev_sign_new), 2000)
    
    def test_new_devset_parallel_to_old_devset(self):
        self.assertSequenceEqual(self.dev_de_old, self.dev_de_new)


    def test_length_testset_timestamps(self):
        self.assertEquals(len(self.test_timestamps), 2000)
    
    def test_length_testset_sign(self):
        self.assertEquals(len(self.test_sign_new), 2000)
    
    def test_new_testset_parallel_to_old_testset(self):
        self.assertSequenceEqual(self.test_de_old, self.test_de_new)
    
    def test_length_train_set(self):
        self.assertEquals(len(self.train_de_new), 48842)
    
    def test_TokenParallelity(self):
        self.assertSequenceEqual(self.line_lengths_sign, self.line_lengths_timestamps)

if __name__ == "__main__":
    unittest.main()