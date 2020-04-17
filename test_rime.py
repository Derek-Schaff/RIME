import back_end.python.rime as rime
import back_end.python.validate as validate
import os.path as path
import unittest
import subprocess
import numpy as np


def write_uint8_to_file(path, arr):
    with open(path, "wb") as f:
        for i in arr:
            f.write(i)


class TestMethods(unittest.TestCase):

    def test_load_binary(self):
        testFilePath = "test/test_bin.bin"
        myArr = np.array([], dtype=np.uint8)
        write_uint8_to_file(testFilePath, myArr)
        testArr = rime.load_binary(testFilePath, "uint8")
        self.assertTrue(np.array_equal(myArr, testArr),"Numpy array written to file and Numpy array read from file should be equal")

    def test_load_binary_empty(self):
        testFilePath = "test/test_bin.bin"
        myArr = np.array([5, 4, 3, 2, 1], dtype=np.uint8)
        write_uint8_to_file(testFilePath, myArr)
        testArr = rime.load_binary(testFilePath, "uint8")
        self.assertTrue(np.array_equal(myArr, testArr),"Numpy array written to file and Numpy array read from file should be equal")

    def test_create_output_dir(self):
        testDir = "test/test_output"
        rime.create_output_dir(testDir)

        self.assertTrue(path.exists(testDir) and path.isdir(testDir), "Output directory test/test_dir should exist")

        # cleanup dir to prevent future tests from getting confused..
        command = "rm -r %s" % testDir
        subprocess.run(command.split())

    def test_resolution_reshape(self):
        inputArr = np.array([1, 1, 1, 1])
        correctArr = np.array([[1, 1], [1, 1]])

        resultArr = rime.resolution_reshape(inputArr, 2, 2)

        self.assertTrue(np.array_equal(correctArr, resultArr), "Input array should be reshaped to match correct array")

    def test_resolution_reshape_valueerror(self):
        inputArr = np.array([1])
        with self.assertRaises(ValueError):
            rime.resolution_reshape(inputArr, 2, 2)

    def test_resolution_reshape_typeerror(self):
        inputArr = []
        with self.assertRaises(TypeError):
            rime.resolution_reshape(inputArr, 2, 2)

    def test_validate_bin_file_exists(self):
        testPath = "test/test_bin.bin"

        self.assertTrue(validate.validate_binary_file(testPath))

    def test_validate_bin_file_doesnt_exist(self):
        testPath = "test/i_dont_exist.bin"

        self.assertFalse(validate.validate_binary_file(testPath))

    def test_validate_np_array_true(self):
        testArr = np.array([1])

        self.assertTrue(validate.validate_np_array(testArr))

    def test_validate_np_array_false(self):
        testArr = [1]

        self.assertFalse(validate.validate_np_array(testArr))


if __name__ == '__main__':
    unittest.main()