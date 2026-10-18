import json
import os
import tempfile
import unittest

from hazim_reseller_agent import (
    generate_listing,
    load_specs,
    validate_inputs,
    InferencePipeline,
)


class TestHazimResellerAgent(unittest.TestCase):

    def test_generate_with_valid_specs(self):
        product = "TestPhone X"
        specs = {
            "condition": "Refurbished",
            "features": ["Unlocked", "Custom ROM installed", "Extended battery"],
            "keywords": ["Android", "Custom ROM", "Unlocked"]
        }
        md = generate_listing(product, specs, local_engine=False)
        self.assertIsInstance(md, str)
        self.assertIn("TestPhone X", md)
        self.assertIn("Key Features", md)
        self.assertIn("Buy Now", md or "")

    def test_validate_inputs_raises_on_empty_product(self):
        with self.assertRaises(ValueError):
            validate_inputs("", {"foo": "bar"})
        with self.assertRaises(ValueError):
            validate_inputs("   ", None)

    def test_load_specs_from_file_and_inline(self):
        inline = '{"condition":"New","keywords":["a","b"]}'
        specs = load_specs(inline)
        self.assertIsInstance(specs, dict)
        self.assertEqual(specs["condition"], "New")

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8")
        try:
            tmp.write(inline)
            tmp.flush()
            tmp.close()
            specs2 = load_specs(tmp.name)
            self.assertIsInstance(specs2, dict)
            self.assertEqual(specs2["condition"], "New")
        finally:
            try:
                os.unlink(tmp.name)
            except Exception:
                pass

    def test_load_specs_corrupted_json_raises(self):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode="w", encoding="utf-8")
        try:
            tmp.write('{"condition": "New", invalid_json}')
            tmp.flush()
            tmp.close()
            with self.assertRaises(ValueError):
                load_specs(tmp.name)
        finally:
            try:
                os.unlink(tmp.name)
            except Exception:
                pass

    def test_generate_handles_empty_specs_gracefully(self):
        product = "MinimalWidget"
        md = generate_listing(product, None, local_engine=False)
        self.assertIsInstance(md, str)
        self.assertIn("MinimalWidget", md)

    def test_inference_pipeline_requires_initialize(self):
        engine = InferencePipeline(local=True)
        with self.assertRaises(RuntimeError):
            engine.infer("x", {})
        engine.initialize()
        out = engine.infer("x", {"condition": "New"})
        self.assertIsInstance(out, dict)
        self.assertIn("seo_title", out)


if __name__ == "__main__":
    unittest.main()
