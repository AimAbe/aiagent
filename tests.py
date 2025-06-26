import unittest
import tempfile
import shutil
import os
import sys
# from subdirectory.filename import function_name
from functions.get_files_info import get_files_info

# Ensure the functions directory is in the path for import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'functions')))

class TestGetFilesInfo(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory with files and a subdirectory
        self.test_dir = tempfile.mkdtemp()
        self.file1 = os.path.join(self.test_dir, "README.md")
        self.file2 = os.path.join(self.test_dir, "package.json")
        self.subdir = os.path.join(self.test_dir, "src")
        os.mkdir(self.subdir)
        with open(self.file1, "w") as f:
            f.write("a" * 10)
        with open(self.file2, "w") as f:
            f.write("b" * 20)
        # Create a file in the subdirectory
        self.subfile = os.path.join(self.subdir, "main.py")
        with open(self.subfile, "w") as f:
            f.write("print('hello')")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_list_root_directory(self):
        result = get_files_info(self.test_dir)
        self.assertIn("- README.md: file_size=10 bytes, is_dir=False", result)
        self.assertIn("- package.json: file_size=20 bytes, is_dir=False", result)
        # Directory size may vary, so just check for the directory entry
        self.assertRegex(result, r"- src: file_size=\d+ bytes, is_dir=True")

    def test_list_subdirectory(self):
        result = get_files_info(self.test_dir, "src")
        self.assertIn("- main.py: file_size=14 bytes, is_dir=False", result)

    def test_directory_outside_working(self):
        outside_dir = "/tmp"
        result = get_files_info(self.test_dir, outside_dir)
        self.assertTrue(result.startswith("Error: Cannot list"))

    def test_nonexistent_directory(self):
        result = get_files_info(self.test_dir, "does_not_exist")
        self.assertTrue(result.startswith("Error: Directory"))

    def test_not_a_directory(self):
        result = get_files_info(self.test_dir, "README.md")
        self.assertTrue(result.startswith('Error: "README.md" is not a directory'))

    def test_print_examples(self):
        print("\n--- get_files_info('calculator', '.') ---")
        print(get_files_info("calculator", "."))
        print("\n--- get_files_info('calculator', 'pkg') ---")
        print(get_files_info("calculator", "pkg"))
        print("\n--- get_files_info('calculator', '/bin') ---")
        print(get_files_info("calculator", "/bin"))
        print("\n--- get_files_info('calculator', '../') ---")
        print(get_files_info("calculator", "../"))

if __name__ == "__main__":
    unittest.main()

