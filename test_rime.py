import back_end.python.rime as rime
import unittest
import numpy as np


class TestMethods(unittest.TestCase):
    def write_uint8_to_file(self, path, arr):
        with open(path, "wb") as f:
            for i in arr:
                f.write(i)

    def test_load_binary(self):
        testFilePath = "test/test_bin.bin"
        myArr = np.array([], dtype=np.uint8)
        self.write_uint8_to_file(testFilePath, myArr)
        testArr = rime.load_binary(testFilePath, "uint8")
        self.assertTrue(np.array_equal(myArr, testArr),"Numpy array written to file and Numpy array read from file should be equal")

        myArr = np.array([5, 4, 3, 2, 1], dtype=np.uint8)
        self.write_uint8_to_file(testFilePath, myArr)
        testArr = rime.load_binary(testFilePath, "uint8")
        self.assertTrue(np.array_equal(myArr, testArr),"Numpy array written to file and Numpy array read from file should be equal")


if __name__ == '__main__':
    unittest.main()