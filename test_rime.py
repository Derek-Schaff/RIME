import back_end.python.rime as rime
import unittest
import numpy as np
import os

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

    def parse_utest(self):
        meta_dic = {"Metadata/Extent/geographic|sw_lon_lat_deg": "-179.999994,-86.716744",
                    "Metadata/ESDR|ESDR_START_YEAR":
                        "1979", "Metadata/DatasetIdentification|VersionID": "v4",
                    "Metadata/Extent/easegrid|grid_units": "meters"}
        rip_dic = {"FT_SESSION_COMPRESS_LEVEL": "4", "FT_SESSION_ENABLE_ISO_METADATA": "True",
                   "FT_SESSION_ESDR_STARTYEAR":
                       "2017", "FT_INPUT_ANC_LAT_PATH": "cell_lat_586x1383_flt32.binIt"}

        print("metadata dicts equal: " + str(
            rime.parse_metadata("/home/turkishdisko/RIME/back_end/python/test/utest_meta") == meta_dic))
        print("ripdic dicts equal: " + str(
            rime.parse_rip("/home/turkishdisko/RIME/back_end/python/test/utest_rip") == rip_dic))

        return


if __name__ == '__main__':
    unittest.main()
