"""Fresh DESIGN contract only: no subprocess or physical run."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import json
import unittest

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / 'src'))
import launch_fresh_references as fresh


class FreshDesignTests(unittest.TestCase):
    def test_original_design_and_no_occupied_reset(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'references'
            write = lambda p, x: p.write_text(json.dumps(x))
            fresh.create_design(root, 17., write)
            before = (root / 'DESIGN.json').read_bytes()
            limit, design = fresh.controller.original_budget(root, lambda p: json.loads(p.read_text()))
            self.assertEqual(limit, 17.)
            self.assertEqual(design['jobs'], [list(j) for j in fresh.controller.JOBS])
            with self.assertRaises(FileExistsError):fresh.create_design(root, 3600., write)
            self.assertEqual((root / 'DESIGN.json').read_bytes(), before)

    def test_bad_budget_rejected_before_creation(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / 'references'
            for value in (0., -1., 3601., float('nan'), float('inf')):
                with self.assertRaises(ValueError):fresh.create_design(root, value, lambda *a: self.fail('no write'))
                self.assertFalse(root.exists())


if __name__ == '__main__':unittest.main()
