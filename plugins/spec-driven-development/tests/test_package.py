import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('validator',ROOT/'scripts/validate_package.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
class PackageTests(unittest.TestCase):
    def test_package_and_missing_reference(self):
        v.validate(ROOT)
        with tempfile.TemporaryDirectory() as d:
            copy=Path(d)/ROOT.name;shutil.copytree(ROOT,copy)
            (copy/'references/contract.md').unlink()
            with self.assertRaises(AssertionError):v.validate(copy)
