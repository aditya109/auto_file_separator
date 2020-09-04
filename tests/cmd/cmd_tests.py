import logging
import os
import shutil
import unittest

import rootpath

from auto_file_separator.cmd.cmd import CMD


class CmdTestMoveFileToFolderMethodWhenLocationIsUnavailable(unittest.TestCase):

    def setUp(self):
        self.mockCMDObject = CMD()
        self.path = rootpath.detect()
        self.test_target_directory = f"{self.path}\\tests\\test_target"
        self.test_file_path = f"{self.test_target_directory}\\test.txt"
        with open(self.test_file_path, "w"):
            pass

    def runTest(self):
        invalid_path = f"{self.test_target_directory}\\invalid_directory"
        test_result = self.mockCMDObject.move_file_to_folder(self.test_file_path, invalid_path)
        self.assertFalse(test_result)

    def tearDown(self) -> None:
        os.remove(self.test_file_path)


class CmdTestMoveFileToFolderMethodWhenLocationIsAvailable(unittest.TestCase):

    def setUp(self):
        self.mockCMDObject = CMD()
        self.path = rootpath.detect()
        self.test_target_directory = f"{self.path}\\tests\\test_target"
        self.test_file_path = f"{self.test_target_directory}\\test.txt"
        os.mkdir(f"{self.test_target_directory}\\pilot")
        with open(self.test_file_path, "w"):
            pass

    def runTest(self):
        valid_path = f"{self.test_target_directory}\\pilot"
        test_result = self.mockCMDObject.move_file_to_folder(self.test_file_path, valid_path)
        self.assertTrue(test_result)

    def tearDown(self) -> None:
        shutil.rmtree(f"{self.test_target_directory}\\pilot")


class CmdTestMoveFileToFolderMethodWhenFileIsUnavailable(unittest.TestCase):

    def setUp(self):
        self.mockCMDObject = CMD()
        self.path = rootpath.detect()
        self.test_target_directory = f"{self.path}\\tests\\test_target"
        os.mkdir(f"{self.test_target_directory}\\pilot")
        self.test_target_directory = f"{self.test_target_directory}\\pilot"

    def runTest(self):
        invalid_file_path = f"{self.test_target_directory}\\test.txt"
        test_result = self.mockCMDObject.move_file_to_folder(invalid_file_path, self.test_target_directory)
        self.assertFalse(test_result)

    def tearDown(self) -> None:
        shutil.rmtree(f"{self.test_target_directory}")


class CmdTestMoveFileToFolderMethodWhenFileIsAvailable(unittest.TestCase):

    def setUp(self):
        self.mockCMDObject = CMD()
        self.path = rootpath.detect()
        self.test_target_directory = f"{self.path}\\tests\\test_target"
        os.mkdir(f"{self.test_target_directory}\\pilot")
        self.valid_file_path = f"{self.test_target_directory}\\test.txt"
        with open(f"{self.test_target_directory}\\test.txt", "w"):
            pass
        self.test_target_directory = f"{self.test_target_directory}\\pilot"

    def runTest(self):
        test_result = self.mockCMDObject.move_file_to_folder(self.valid_file_path, self.test_target_directory)
        self.assertTrue(test_result)

    def tearDown(self) -> None:
        shutil.rmtree(f"{self.test_target_directory}")


class CmdTestGetExtensionsList(unittest.TestCase):

    def setUp(self) -> None:
        self.mockCMDObject = CMD()
        self.numberOfExtensionsTypes = self.mockCMDObject.get_config()

    def runTest(self):
        test_result = self.mockCMDObject.get_extensions_list()
        self.assertTrue(
            len(test_result.keys()) == len(self.numberOfExtensionsTypes["locations"]["div-directories"].split("|")))


class CmdTestGetLoggerObject(unittest.TestCase):
    def setUp(self) -> None:
        self.mockCMDObject = CMD()

    def runTest(self):
        test_result = self.mockCMDObject.get_logger()
        self.assertTrue(isinstance(test_result, logging.Logger))


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(CmdTestMoveFileToFolderMethodWhenLocationIsUnavailable())
    suite.addTest(CmdTestMoveFileToFolderMethodWhenLocationIsAvailable())
    suite.addTest(CmdTestMoveFileToFolderMethodWhenFileIsUnavailable())
    suite.addTest(CmdTestMoveFileToFolderMethodWhenFileIsUnavailable())
    suite.addTest(CmdTestGetExtensionsList())
    suite.addTest(CmdTestGetLoggerObject())
    unittest.TextTestRunner().run(suite)
