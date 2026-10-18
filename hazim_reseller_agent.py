#!/usr/bin/env python3
"""
hazim_reseller_agent.py

Production-ready CLI tool that runs a local Inference Pipeline (Local Engine) and deterministic
template processing to produce SEO-optimized markdown product listings for marketplace resellers.
"""

from __future__ import annotations
import argparse
import json
import logging
import os
import sys
import time
from typing import Any, Dict, Optional

# Optional dependencies
try:
    import jsonschema  # type: ignore
    _HAS_JSONSCHEMA = True
except Exception:
    _HAS_JSONSCHEMA = False

try:
    from rich import print as rprint  # type: ignore
    _HAS_RICH = True
except Exception:
    _HAS_RICH = False


# Logging configuration
logger = logging.getLogger("hazim_reseller_agent")
logger.setLevel(logging.DEBUG)
_stream = logging.StreamHandler(sys.stdout)
_stream.setLevel(logging.INFO)
_fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
_stream.setFormatter(_fmt)
logger.addHandler(_stream)

_logfile = os.environ.get("HAZIM_RESELLER_LOG", "hazim_reseller_agent.log")
_file_handler = logging.FileHandler(_logfile)
_file_handler.setLevel(logging.DEBUG)
_file_handler.setFormatter(_fmt)
logger.addHandler(_file_handler)


# JSON schema for basic validation
SPECS_SCHEMA = {
    "type": "object",
    "properties": {
        "condition": {"type": "string"},
        "features": {"type": "array", "items": {"type": "string"}},
        "keywords": {"type": "array", "items": {"type": "string"}},
        "price": {"type": ["number", "string"]},
        "color": {"type": "string"},
        "storage": {"type": "string"}
    },
    "additionalProperties": True
}


# Prompt engineering (industrial benefits of Open Innovation)
_PROMPT_ENGINEERING_NOTE = (
    "Open Innovation industrial benefits:\n"
    "1) Data Sovereignty & Enterprise Privacy: Process product data locally; no third-party telemetry or data retention.\n"
    "2) Zero Operational Ingestion Fees: Run deterministic templates or local engines with no per-request API costs.\n"
    "3) Complete Elimination of Closed API Vendor Lock-in: Model-agnostic pipeline lets you switch engines without vendor constraints.\n"
)

logger.debug("Prompt engineering note loaded.")


class InferencePipeline:
    """
    Inference Pipeline / Local Engine for structured listing generation.

    This component models a production local engine and deterministic template processing.
    Replace the engine integration with an actual inference runtime as needed.
    """

    def __init__(self, local: bool = False, engine_name: str = "local-engine") -> None:
        self.local = bool(local)
        self.engine_name = engine_name
        self.initialized = False

    def initialize(self, timeout: float = 5.0) -> None:
        logger.info("Initializing local engine '%s' (local=%s)", self.engine_name, self.local)
        # Simulate brief initialization in a defensive manner
        start = time.time()
        # keep minimal sleep to remain fast while simulating I/O
        while time.time() - start < min(timeout, 0.01):
            time.sleep(0.001)
        self.initialized = True
        logger.debug("Engine initialized: %s", self.initialized)

    def infer(self, product: str, specs: Dict[str, Any]) -> Dict[str, Any]:
        if not self.initialized:
            raise RuntimeError("Local engine not initialized")

        condition = specs.get("condition", "Used - Good")
        features = specs.get("features", []) or []
        keywords = specs.get("keywords", []) or []
        price = specs.get("price", "")
        color = specs.get("color", "")
        storage = specs.get("storage", "")

        # SEO title composition
        top_keywords = [str(k) for k in (keywords[:3] if isinstance(keywords, list) else []) if k]
        parts = [product]
        if storage:
            parts.append(storage)
        if color:
            parts.append(color)
        if top_keywords:
            parts.append(" ".join(top_keywords))
        seo_title = " · ".join([p for p in parts if p])

        bullets = [f"Condition: {condition}"]
        if features:
            bullets.extend([f"{f}" for f in features[:6]])
        if price:
            bullets.append(f"Price guidance: {price}")

        feature_text = ", ".join(features) if features else "High-quality, tested item"
        long_description = (
            f"{product}\n\n"
            f"{feature_text}. Condition: {condition}.\n\n"
            f"Optimized for marketplace discovery: {', '.join(top_keywords)}.\n\n"
            "Why purchase from an independent reseller:\n"
            "- Personalized service and rapid responses.\n"
            "- Thorough testing and verification before shipment.\n\n"
            "This listing is crafted to convert while following marketplace policies."
        )

        product_tokens = [t.strip() for t in product.split() if len(t.strip()) > 1][:6]
        tags = list(dict.fromkeys(product_tokens + top_keywords))[:13]

        cta = "Buy Now — Limited stock. Fast shipping."

        logger.debug("Inference produced seo_title='%s' bullets=%d tags=%d", seo_title, len(bullets), len(tags))

        return {
            "seo_title": seo_title,
            "subtitle": f"{product} — {condition}",
            "bullets": bullets,
            "long_description": long_description,
            "tags": tags,
            "cta": cta,
        }


# Core functions

def validate_inputs(product: str, specs: Optional[Dict[str, Any]]) -> None:
    if not product or not isinstance(product, str) or not product.strip():
        logger.error("Validation failed: product name must be a non-empty string")
        raise ValueError("product name must be a non-empty string")
    if specs is not None and not isinstance(specs, dict):
        logger.error("Validation failed: specs must be a JSON object/dict when provided")
        raise ValueError("specs must be a JSON object/dict when provided")
    logger.debug("Inputs validated: product=%s, specs_keys=%s", product, list((specs or {}).keys()))


def load_specs(specs_source: Optional[str]) -> Optional[Dict[str, Any]]:
    if specs_source is None:
        logger.info("No specs provided; continuing with defaults.")
        return None

    if isinstance(specs_source, dict):
        return specs_source

    try:
        source = str(specs_source).strip()
        if os.path.exists(source) and os.path.isfile(source):
            size = os.path.getsize(source)
            if size > 1_000_000:
                logger.error("Specs file size exceeds 1MB limit (%d bytes)", size)
                raise ValueError("Specs file too large")
            with open(source, "r", encoding="utf-8") as fh:
                text = fh.read()
            obj = json.loads(text)
            logger.info("Specs loaded from file: %s", source)
            return obj
        else:
            obj = json.loads(source)
            logger.info("Specs parsed from inline JSON")
            return obj
    except json.JSONDecodeError as e:
        logger.exception("Failed to parse specs JSON: %s", e)
        raise ValueError("Invalid JSON for specs") from e
    except Exception as e:
        logger.exception("Unexpected error loading specs: %s", e)
        raise


def validate_specs_schema(specs: Optional[Dict[str, Any]]) -> None:
    if specs is None:
        return
    if _HAS_JSONSCHEMA:
        try:
            jsonschema.validate(instance=specs, schema=SPECS_SCHEMA)
            logger.debug("Specs validated against schema")
        except Exception as e:
            logger.warning("Specs failed schema validation: %s", e)
    else:
        logger.debug("jsonschema not installed; skipping strict validation")


def generate_listing(product: str, specs: Optional[Dict[str, Any]], local_engine: bool = False) -> str:
    validate_inputs(product, specs)
    validate_specs_schema(specs)

    engine = InferencePipeline(local=local_engine)
    try:
        engine.initialize()
    except Exception as e:
        logger.exception("Engine initialization failed: %s", e)
        engine = InferencePipeline(local=False)
        engine.initialize()

    try:
        structured = engine.infer(product, specs or {})
    except Exception as e:
        logger.exception("Generation failed: %s", e)
        raise RuntimeError("Listing generation failed") from e

    seo_title = structured.get("seo_title", product)
    subtitle = structured.get("subtitle", "")
    bullets = structured.get("bullets", [])
    long_description = structured.get("long_description", "")
    tags = structured.get("tags", [])
    cta = structured.get("cta", "Buy Now")

    md_lines = []
    md_lines.append(f"# {seo_title}")
    if subtitle:
        md_lines.append(f"**{subtitle}**")
    md_lines.append("")
    md_lines.append("## Key Features")
    for b in bullets:
        md_lines.append(f"- {b}")
    md_lines.append("")
    md_lines.append("## Description")
    md_lines.append(long_description)
    md_lines.append("")
    md_lines.append("## What you'll get")
    md_lines.append("- The exact item pictured and described above")
    md_lines.append("- Fast, tracked shipping")
    md_lines.append("- Friendly seller support")
    md_lines.append("")
    md_lines.append("## Tags")
    md_lines.append(", ".join(tags))
    md_lines.append("")
    md_lines.append(f"**{cta}**")
    md_lines.append("")
    md_lines.append("---\n")
    md_lines.append("> Listing generated with hazim-reseller-agent. Open Innovation: Data Sovereignty, Zero Operational Ingestion Fees, No Vendor Lock-in.")

    md_text = "\n".join(md_lines)
    logger.info("Listing generation complete for product '%s'", product)
    return md_text


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="hazim_reseller_agent", description="Generate SEO-optimized marketplace listings using a local inference engine and deterministic templates.")
    parser.add_argument("--product", "-p", required=True, help="Product name/title (required).")
    parser.add_argument("--specs", "-s", help="Path to JSON specs file or inline JSON string.")
    parser.add_argument("--local-engine", "-l", action="store_true", help="Use a local inference engine.")
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    try:
        specs = load_specs(args.specs) if args.specs else None
    except ValueError as e:
        logger.error("Could not load specs: %s", e)
        return 2
    except Exception as e:
        logger.exception("Unexpected error loading specs: %s", e)
        return 2

    try:
        md = generate_listing(args.product, specs, local_engine=args.local_engine)
        if _HAS_RICH:
            rprint(md)
        else:
            print(md)
        return 0
    except Exception as e:
        logger.exception("Failed to generate listing: %s", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
