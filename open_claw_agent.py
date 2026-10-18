#!/usr/bin/env python3
"""
Compatibility shim for older entrypoints.
"""
from hazim_reseller_agent import main
import sys

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
